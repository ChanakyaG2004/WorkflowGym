from dataclasses import dataclass

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


REQUIRED_FINANCE_TOOLS = [
    "get_customer",
    "get_invoice",
    "get_usage_events",
    "get_contract_terms",
    "compare_usage_to_invoice",
]


@dataclass(frozen=True)
class ScenarioFixture:
    scenario_key: str
    customer_name: str
    month: str
    prompt: str
    expected_outcome: str
    hidden_cause: str
    included_api_calls: int
    overage_rate_cents: int
    valid_usage_quantity: int
    duplicate_usage_quantity: int
    invoice_usage_quantity: int
    invoice_unit_price_cents: int
    invoice_amount_cents: int


SCENARIO_FIXTURES = [
    ScenarioFixture(
        scenario_key="duplicate_usage_001",
        customer_name="Acme AI",
        month="2026-06",
        prompt="Acme AI says its June 2026 invoice is too high.",
        expected_outcome="invoice_incorrect",
        hidden_cause="duplicate_usage_events",
        included_api_calls=100_000,
        overage_rate_cents=4,
        valid_usage_quantity=150_000,
        duplicate_usage_quantity=50_000,
        invoice_usage_quantity=200_000,
        invoice_unit_price_cents=4,
        invoice_amount_cents=400_000,
    ),
    ScenarioFixture(
        scenario_key="overage_rate_mismatch_001",
        customer_name="Beta Robotics",
        month="2026-07",
        prompt="Beta Robotics says its July 2026 invoice used the wrong overage rate.",
        expected_outcome="invoice_incorrect",
        hidden_cause="overage_rate_mismatch",
        included_api_calls=100_000,
        overage_rate_cents=4,
        valid_usage_quantity=180_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=180_000,
        invoice_unit_price_cents=6,
        invoice_amount_cents=480_000,
    ),
    ScenarioFixture(
        scenario_key="included_allowance_not_applied_001",
        customer_name="CloudCart",
        month="2026-08",
        prompt="CloudCart says its August 2026 invoice ignored its included API calls.",
        expected_outcome="invoice_incorrect",
        hidden_cause="included_allowance_not_applied",
        included_api_calls=100_000,
        overage_rate_cents=4,
        valid_usage_quantity=120_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=120_000,
        invoice_unit_price_cents=4,
        invoice_amount_cents=480_000,
    ),
    ScenarioFixture(
        scenario_key="below_allowance_overage_001",
        customer_name="Delta Design",
        month="2026-09",
        prompt="Delta Design says it was charged overage despite staying below allowance.",
        expected_outcome="invoice_incorrect",
        hidden_cause="below_allowance_overage_charged",
        included_api_calls=100_000,
        overage_rate_cents=4,
        valid_usage_quantity=80_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=80_000,
        invoice_unit_price_cents=4,
        invoice_amount_cents=80_000,
    ),
    ScenarioFixture(
        scenario_key="invoice_usage_exceeds_records_001",
        customer_name="Echo Health",
        month="2026-10",
        prompt="Echo Health says its October 2026 invoice shows more usage than records.",
        expected_outcome="invoice_incorrect",
        hidden_cause="invoice_usage_exceeds_recorded_usage",
        included_api_calls=100_000,
        overage_rate_cents=4,
        valid_usage_quantity=130_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=160_000,
        invoice_unit_price_cents=4,
        invoice_amount_cents=240_000,
    ),
    ScenarioFixture(
        scenario_key="invoice_correct_001",
        customer_name="Fairwind Labs",
        month="2026-11",
        prompt="Fairwind Labs asks whether its November 2026 invoice is correct.",
        expected_outcome="invoice_correct",
        hidden_cause="no_issue_found",
        included_api_calls=100_000,
        overage_rate_cents=4,
        valid_usage_quantity=150_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=150_000,
        invoice_unit_price_cents=4,
        invoice_amount_cents=200_000,
    ),
    ScenarioFixture(
        scenario_key="duplicate_usage_002",
        customer_name="Granite Analytics",
        month="2026-12",
        prompt="Granite Analytics says its December 2026 invoice includes repeated usage.",
        expected_outcome="invoice_incorrect",
        hidden_cause="duplicate_usage_events",
        included_api_calls=150_000,
        overage_rate_cents=3,
        valid_usage_quantity=220_000,
        duplicate_usage_quantity=30_000,
        invoice_usage_quantity=250_000,
        invoice_unit_price_cents=3,
        invoice_amount_cents=300_000,
    ),
    ScenarioFixture(
        scenario_key="duplicate_usage_003",
        customer_name="Helio Maps",
        month="2027-01",
        prompt="Helio Maps says its January 2027 invoice double-counted a usage import.",
        expected_outcome="invoice_incorrect",
        hidden_cause="duplicate_usage_events",
        included_api_calls=50_000,
        overage_rate_cents=2,
        valid_usage_quantity=75_000,
        duplicate_usage_quantity=25_000,
        invoice_usage_quantity=100_000,
        invoice_unit_price_cents=2,
        invoice_amount_cents=100_000,
    ),
    ScenarioFixture(
        scenario_key="duplicate_usage_004",
        customer_name="Ion Security",
        month="2027-02",
        prompt="Ion Security says its February 2027 invoice includes duplicated API events.",
        expected_outcome="invoice_incorrect",
        hidden_cause="duplicate_usage_events",
        included_api_calls=200_000,
        overage_rate_cents=5,
        valid_usage_quantity=260_000,
        duplicate_usage_quantity=40_000,
        invoice_usage_quantity=300_000,
        invoice_unit_price_cents=5,
        invoice_amount_cents=500_000,
    ),
    ScenarioFixture(
        scenario_key="overage_rate_mismatch_002",
        customer_name="Jupiter Supply",
        month="2027-03",
        prompt="Jupiter Supply says its March 2027 overage rate is higher than contract.",
        expected_outcome="invoice_incorrect",
        hidden_cause="overage_rate_mismatch",
        included_api_calls=100_000,
        overage_rate_cents=5,
        valid_usage_quantity=140_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=140_000,
        invoice_unit_price_cents=7,
        invoice_amount_cents=280_000,
    ),
    ScenarioFixture(
        scenario_key="overage_rate_mismatch_003",
        customer_name="Keystone Legal",
        month="2027-04",
        prompt="Keystone Legal says its April 2027 invoice used a rate from the wrong plan.",
        expected_outcome="invoice_incorrect",
        hidden_cause="overage_rate_mismatch",
        included_api_calls=200_000,
        overage_rate_cents=3,
        valid_usage_quantity=260_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=260_000,
        invoice_unit_price_cents=4,
        invoice_amount_cents=240_000,
    ),
    ScenarioFixture(
        scenario_key="overage_rate_mismatch_004",
        customer_name="Lumen Retail",
        month="2027-05",
        prompt="Lumen Retail says its May 2027 overage was priced above contract.",
        expected_outcome="invoice_incorrect",
        hidden_cause="overage_rate_mismatch",
        included_api_calls=50_000,
        overage_rate_cents=8,
        valid_usage_quantity=90_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=90_000,
        invoice_unit_price_cents=10,
        invoice_amount_cents=400_000,
    ),
    ScenarioFixture(
        scenario_key="included_allowance_not_applied_002",
        customer_name="Meridian Bio",
        month="2027-06",
        prompt="Meridian Bio says its June 2027 invoice charged all usage, not just overage.",
        expected_outcome="invoice_incorrect",
        hidden_cause="included_allowance_not_applied",
        included_api_calls=250_000,
        overage_rate_cents=2,
        valid_usage_quantity=300_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=300_000,
        invoice_unit_price_cents=2,
        invoice_amount_cents=600_000,
    ),
    ScenarioFixture(
        scenario_key="included_allowance_not_applied_003",
        customer_name="Northstar CRM",
        month="2027-07",
        prompt="Northstar CRM says its July 2027 invoice did not subtract included calls.",
        expected_outcome="invoice_incorrect",
        hidden_cause="included_allowance_not_applied",
        included_api_calls=75_000,
        overage_rate_cents=6,
        valid_usage_quantity=110_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=110_000,
        invoice_unit_price_cents=6,
        invoice_amount_cents=660_000,
    ),
    ScenarioFixture(
        scenario_key="below_allowance_overage_002",
        customer_name="Orchid Finance",
        month="2027-08",
        prompt="Orchid Finance says it was billed overage while under its August allowance.",
        expected_outcome="invoice_incorrect",
        hidden_cause="below_allowance_overage_charged",
        included_api_calls=250_000,
        overage_rate_cents=2,
        valid_usage_quantity=200_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=200_000,
        invoice_unit_price_cents=2,
        invoice_amount_cents=100_000,
    ),
    ScenarioFixture(
        scenario_key="below_allowance_overage_003",
        customer_name="Pioneer EdTech",
        month="2027-09",
        prompt="Pioneer EdTech says its September 2027 invoice charged overage below allowance.",
        expected_outcome="invoice_incorrect",
        hidden_cause="below_allowance_overage_charged",
        included_api_calls=500_000,
        overage_rate_cents=1,
        valid_usage_quantity=450_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=450_000,
        invoice_unit_price_cents=1,
        invoice_amount_cents=50_000,
    ),
    ScenarioFixture(
        scenario_key="invoice_usage_exceeds_records_002",
        customer_name="Quartz Media",
        month="2027-10",
        prompt="Quartz Media says its October 2027 invoice has more calls than usage logs.",
        expected_outcome="invoice_incorrect",
        hidden_cause="invoice_usage_exceeds_recorded_usage",
        included_api_calls=100_000,
        overage_rate_cents=4,
        valid_usage_quantity=170_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=210_000,
        invoice_unit_price_cents=4,
        invoice_amount_cents=440_000,
    ),
    ScenarioFixture(
        scenario_key="invoice_usage_exceeds_records_003",
        customer_name="RiverOps",
        month="2027-11",
        prompt="RiverOps says its November 2027 invoice includes usage not in records.",
        expected_outcome="invoice_incorrect",
        hidden_cause="invoice_usage_exceeds_recorded_usage",
        included_api_calls=300_000,
        overage_rate_cents=2,
        valid_usage_quantity=330_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=420_000,
        invoice_unit_price_cents=2,
        invoice_amount_cents=240_000,
    ),
    ScenarioFixture(
        scenario_key="invoice_correct_002",
        customer_name="Summit Travel",
        month="2027-12",
        prompt="Summit Travel asks whether its December 2027 invoice matches contract terms.",
        expected_outcome="invoice_correct",
        hidden_cause="no_issue_found",
        included_api_calls=200_000,
        overage_rate_cents=3,
        valid_usage_quantity=240_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=240_000,
        invoice_unit_price_cents=3,
        invoice_amount_cents=120_000,
    ),
    ScenarioFixture(
        scenario_key="invoice_correct_003",
        customer_name="Terra Foods",
        month="2028-01",
        prompt="Terra Foods asks whether its January 2028 invoice is correct.",
        expected_outcome="invoice_correct",
        hidden_cause="no_issue_found",
        included_api_calls=100_000,
        overage_rate_cents=4,
        valid_usage_quantity=70_000,
        duplicate_usage_quantity=0,
        invoice_usage_quantity=70_000,
        invoice_unit_price_cents=4,
        invoice_amount_cents=0,
    ),
]


def _seed_fixture(fixture: ScenarioFixture) -> None:
    db = SessionLocal()
    try:
        existing = db.scalar(
            select(Scenario).where(Scenario.scenario_key == fixture.scenario_key)
        )
        if existing is not None:
            return

        customer = Customer(name=fixture.customer_name)
        db.add(customer)
        db.flush()

        db.add(
            PricingPlan(
                customer_id=customer.id,
                included_api_calls=fixture.included_api_calls,
                overage_rate_cents=fixture.overage_rate_cents,
            )
        )

        usage_events = [
            UsageEvent(
                customer_id=customer.id,
                month=fixture.month,
                event_type="api_calls",
                quantity=fixture.valid_usage_quantity,
                is_duplicate=False,
            )
        ]
        if fixture.duplicate_usage_quantity:
            usage_events.append(
                UsageEvent(
                    customer_id=customer.id,
                    month=fixture.month,
                    event_type="api_calls",
                    quantity=fixture.duplicate_usage_quantity,
                    is_duplicate=True,
                )
            )
        db.add_all(usage_events)

        invoice = Invoice(
            customer_id=customer.id,
            month=fixture.month,
            total_cents=fixture.invoice_amount_cents,
        )
        db.add(invoice)
        db.flush()

        db.add(
            InvoiceLineItem(
                invoice_id=invoice.id,
                description=f"API call usage for {fixture.month}",
                quantity=fixture.invoice_usage_quantity,
                unit_price_cents=fixture.invoice_unit_price_cents,
                amount_cents=fixture.invoice_amount_cents,
            )
        )

        db.add(
            Scenario(
                scenario_key=fixture.scenario_key,
                customer_name=fixture.customer_name,
                month=fixture.month,
                prompt=fixture.prompt,
                expected_outcome=fixture.expected_outcome,
                hidden_cause=fixture.hidden_cause,
                required_tools=REQUIRED_FINANCE_TOOLS,
            )
        )

        db.commit()
    finally:
        db.close()


def seed_acme(reset: bool = True) -> None:
    """Seed all demo FinanceOps scenarios.

    The original function name is kept for backwards compatibility with the
    earlier one-scenario version of the project.
    """
    if reset:
        reset_db()

    for fixture in SCENARIO_FIXTURES:
        _seed_fixture(fixture)


def seed_acme_if_missing() -> None:
    """Seed demo scenarios without resetting existing run history."""
    seed_acme(reset=False)


if __name__ == "__main__":
    seed_acme()
    print(f"Seeded {len(SCENARIO_FIXTURES)} WorkflowGym scenarios.")
