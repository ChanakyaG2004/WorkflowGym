import os


os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:////tmp/workflowgym_pytest.db")

from sqlalchemy import select

from app.agents.rule_based_agent import run_rule_based_agent
from app.db.database import SessionLocal
from app.db.models import Scenario
from app.evaluation.evaluator import evaluate_run
from app.main import get_metrics_summary, run_scenario
from app.seed.seed_acme import seed_acme
from app.tools.finance_tools import compare_usage_to_invoice, get_customer


def test_finance_tool_detects_duplicate_usage_overcharge():
    seed_acme()
    db = SessionLocal()
    try:
        customer = get_customer(db, "Acme AI")["customer"]
        comparison = compare_usage_to_invoice(
            db,
            customer_id=customer["id"],
            month="2026-06",
        )
    finally:
        db.close()

    assert comparison["invoice_incorrect"] is True
    assert comparison["cause"] == "duplicate_usage_events"
    assert comparison["valid_usage_quantity"] == 150_000
    assert comparison["duplicate_usage_quantity"] == 50_000
    assert comparison["correct_billable_overage_calls"] == 50_000
    assert comparison["actual_charged_overage_calls"] == 100_000
    assert comparison["overcharge_cents"] == 200_000


def test_agent_run_stores_trace_and_metrics():
    seed_acme()
    db = SessionLocal()
    try:
        scenario = db.scalar(
            select(Scenario).where(Scenario.scenario_key == "duplicate_usage_001")
        )
        run = run_rule_based_agent(db, scenario)
        result = evaluate_run(db, run, scenario)

        assert run.status == "completed"
        assert run.final_answer["decision"] == "invoice_incorrect"
        assert run.final_answer["cause"] == "duplicate_usage_events"
        assert len(run.steps) == 5
        assert result.passed is True
        assert result.score == 100
        assert result.tool_accuracy == 100
        assert result.called_required_tool_count == 5
        assert result.total_tool_call_count == 5
        assert result.duplicate_usage_quantity == 50_000
        assert result.detected_overcharge_cents == 200_000
    finally:
        db.close()


def test_metrics_summary_reports_portfolio_numbers():
    seed_acme()
    db = SessionLocal()
    try:
        run_scenario("duplicate_usage_001", db)
        summary = get_metrics_summary(db)
    finally:
        db.close()

    assert summary.total_scenarios == 1
    assert summary.total_runs == 1
    assert summary.passed_runs == 1
    assert summary.pass_rate == 100.0
    assert summary.average_score == 100.0
    assert summary.average_tool_accuracy == 100.0
    assert summary.total_tool_calls == 5
    assert summary.total_detected_overcharge_cents == 200_000
    assert summary.total_duplicate_usage_quantity == 50_000
