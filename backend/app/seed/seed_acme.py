from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.init_db import reset_db
from app.db.models import (
    Customer,
    Invoice,
    InvoiceLineItem,
    PricingPlan,
    Scenario,
    UsageEvent,
)


def seed_acme(reset: bool = True) -> None:
    """Create the Acme AI duplicate usage scenario.

    reset=True is useful for repeatable local demos and tests. Deployments can
    pass reset=False to avoid deleting existing run history.
    """
    if reset:
        reset_db()

    db = SessionLocal()
    try:
        existing = db.scalar(
            select(Scenario).where(Scenario.scenario_key == "duplicate_usage_001")
        )
        if existing is not None:
            return

        customer = Customer(name="Acme AI")
        db.add(customer)
        db.flush()

        db.add(
            PricingPlan(
                customer_id=customer.id,
                included_api_calls=100_000,
                overage_rate_cents=4,
            )
        )

        db.add_all(
            [
                UsageEvent(
                    customer_id=customer.id,
                    month="2026-06",
                    event_type="api_calls",
                    quantity=150_000,
                    is_duplicate=False,
                ),
                UsageEvent(
                    customer_id=customer.id,
                    month="2026-06",
                    event_type="api_calls",
                    quantity=50_000,
                    is_duplicate=True,
                ),
            ]
        )

        invoice = Invoice(
            customer_id=customer.id,
            month="2026-06",
            total_cents=400_000,
        )
        db.add(invoice)
        db.flush()

        db.add(
            InvoiceLineItem(
                invoice_id=invoice.id,
                description="API call usage for June 2026",
                quantity=200_000,
                unit_price_cents=4,
                amount_cents=400_000,
            )
        )

        db.add(
            Scenario(
                scenario_key="duplicate_usage_001",
                customer_name="Acme AI",
                month="2026-06",
                prompt="Acme AI says its June 2026 invoice is too high.",
                expected_outcome="invoice_incorrect",
                hidden_cause="duplicate_usage_events",
                required_tools=[
                    "get_customer",
                    "get_invoice",
                    "get_usage_events",
                    "get_contract_terms",
                    "compare_usage_to_invoice",
                ],
            )
        )

        db.commit()
    finally:
        db.close()


def seed_acme_if_missing() -> None:
    """Seed the demo scenario without resetting existing data."""
    seed_acme(reset=False)


if __name__ == "__main__":
    seed_acme()
    print("Seeded Acme AI scenario: duplicate_usage_001")
