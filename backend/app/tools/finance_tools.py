from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Customer, Invoice, PricingPlan, UsageEvent


def get_customer(db: Session, customer_name: str) -> dict[str, Any]:
    """Find a customer by name."""
    customer = db.scalar(select(Customer).where(Customer.name == customer_name))
    if customer is None:
        return {"found": False, "customer": None}

    return {"found": True, "customer": {"id": customer.id, "name": customer.name}}


def get_invoice(db: Session, customer_id: int, month: str) -> dict[str, Any]:
    """Load a customer's invoice and line items for one month."""
    invoice = db.scalar(
        select(Invoice).where(
            Invoice.customer_id == customer_id,
            Invoice.month == month,
        )
    )
    if invoice is None:
        return {"found": False, "invoice": None}

    return {
        "found": True,
        "invoice": {
            "id": invoice.id,
            "customer_id": invoice.customer_id,
            "month": invoice.month,
            "total_cents": invoice.total_cents,
            "line_items": [
                {
                    "id": item.id,
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price_cents": item.unit_price_cents,
                    "amount_cents": item.amount_cents,
                }
                for item in invoice.line_items
            ],
        },
    }


def get_usage_events(db: Session, customer_id: int, month: str) -> dict[str, Any]:
    """Load usage events for one customer and month."""
    events = db.scalars(
        select(UsageEvent).where(
            UsageEvent.customer_id == customer_id,
            UsageEvent.month == month,
        )
    ).all()

    return {
        "events": [
            {
                "id": event.id,
                "event_type": event.event_type,
                "quantity": event.quantity,
                "is_duplicate": event.is_duplicate,
            }
            for event in events
        ],
        "total_quantity": sum(event.quantity for event in events),
        "duplicate_quantity": sum(event.quantity for event in events if event.is_duplicate),
        "valid_quantity": sum(event.quantity for event in events if not event.is_duplicate),
    }


def get_contract_terms(db: Session, customer_id: int) -> dict[str, Any]:
    """Load the customer's current pricing plan."""
    plan = db.scalar(select(PricingPlan).where(PricingPlan.customer_id == customer_id))
    if plan is None:
        return {"found": False, "pricing_plan": None}

    return {
        "found": True,
        "pricing_plan": {
            "included_api_calls": plan.included_api_calls,
            "overage_rate_cents": plan.overage_rate_cents,
        },
    }


def compare_usage_to_invoice(db: Session, customer_id: int, month: str) -> dict[str, Any]:
    """Compare valid usage and contract terms against the invoice charges."""
    usage = get_usage_events(db, customer_id=customer_id, month=month)
    contract = get_contract_terms(db, customer_id=customer_id)
    invoice_result = get_invoice(db, customer_id=customer_id, month=month)

    if not contract["found"] or not invoice_result["found"]:
        return {"comparison_possible": False}

    plan = contract["pricing_plan"]
    invoice = invoice_result["invoice"]
    included_calls = plan["included_api_calls"]
    overage_rate_cents = plan["overage_rate_cents"]

    valid_quantity = usage["valid_quantity"]
    total_recorded_quantity = usage["total_quantity"]
    api_line_items = [
        item
        for item in invoice["line_items"]
        if "api" in item["description"].lower()
    ]
    invoiced_quantity = sum(item["quantity"] for item in api_line_items)
    actual_overage_cents = sum(
        item["amount_cents"] for item in api_line_items if item["amount_cents"] > 0
    )
    invoice_unit_price_cents = (
        api_line_items[0]["unit_price_cents"] if api_line_items else overage_rate_cents
    )

    correct_overage_calls = max(valid_quantity - included_calls, 0)
    actual_charged_overage_calls = (
        actual_overage_cents // invoice_unit_price_cents
        if invoice_unit_price_cents > 0
        else 0
    )
    expected_overage_cents = correct_overage_calls * overage_rate_cents

    invoice_incorrect = actual_overage_cents != expected_overage_cents

    if not invoice_incorrect:
        cause = "no_issue_found"
    elif usage["duplicate_quantity"] > 0 and invoiced_quantity > valid_quantity:
        cause = "duplicate_usage_events"
    elif valid_quantity < included_calls and actual_overage_cents > 0:
        cause = "below_allowance_overage_charged"
    elif invoiced_quantity > total_recorded_quantity:
        cause = "invoice_usage_exceeds_recorded_usage"
    elif (
        invoice_unit_price_cents != overage_rate_cents
        and actual_charged_overage_calls == correct_overage_calls
    ):
        cause = "overage_rate_mismatch"
    elif (
        valid_quantity > included_calls
        and invoiced_quantity == valid_quantity
        and actual_charged_overage_calls == valid_quantity
    ):
        cause = "included_allowance_not_applied"
    else:
        cause = "incorrect_overage_calculation"

    return {
        "comparison_possible": True,
        "invoice_incorrect": invoice_incorrect,
        "cause": cause,
        "valid_usage_quantity": valid_quantity,
        "total_recorded_usage_quantity": total_recorded_quantity,
        "duplicate_usage_quantity": usage["duplicate_quantity"],
        "invoice_usage_quantity": invoiced_quantity,
        "included_api_calls": included_calls,
        "contract_overage_rate_cents": overage_rate_cents,
        "invoice_unit_price_cents": invoice_unit_price_cents,
        "correct_billable_overage_calls": correct_overage_calls,
        "actual_charged_overage_calls": actual_charged_overage_calls,
        "expected_overage_cents": expected_overage_cents,
        "actual_overage_cents": actual_overage_cents,
        "overcharge_cents": actual_overage_cents - expected_overage_cents,
    }
