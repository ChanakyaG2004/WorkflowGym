from sqlalchemy import select

from app.agents.rule_based_agent import run_rule_based_agent
from app.db.database import SessionLocal
from app.db.models import Scenario
from app.evaluation.evaluator import evaluate_run
from app.seed.seed_acme import seed_acme


def main() -> None:
    """Seed Acme AI, run the scenario, and verify the expected pass result."""
    seed_acme()

    db = SessionLocal()
    try:
        scenario = db.scalar(
            select(Scenario).where(Scenario.scenario_key == "duplicate_usage_001")
        )
        if scenario is None:
            raise RuntimeError("Scenario duplicate_usage_001 was not seeded.")

        run = run_rule_based_agent(db, scenario)
        result = evaluate_run(db, run, scenario)

        if not result.passed:
            raise RuntimeError(f"Smoke test failed: {result.details}")

        print(
            {
                "scenario": scenario.scenario_key,
                "run_id": run.id,
                "decision": run.final_answer["decision"] if run.final_answer else None,
                "cause": run.final_answer["cause"] if run.final_answer else None,
                "score": result.score,
                "tool_accuracy": result.tool_accuracy,
                "required_tools_called": (
                    f"{result.called_required_tool_count}/"
                    f"{result.required_tool_count}"
                ),
                "tool_calls_traced": result.total_tool_call_count,
                "duplicate_usage_detected": result.duplicate_usage_quantity,
                "overcharge_detected_dollars": result.detected_overcharge_cents / 100,
                "run_duration_ms": result.run_duration_ms,
                "passed": result.passed,
            }
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
