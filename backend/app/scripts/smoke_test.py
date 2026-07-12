from sqlalchemy import select

from app.agents.rule_based_agent import run_rule_based_agent
from app.db.database import SessionLocal
from app.db.models import Scenario
from app.evaluation.evaluator import evaluate_run
from app.seed.seed_acme import seed_acme


def main() -> None:
    """Seed demo data, run all scenarios, and verify the expected pass results."""
    seed_acme()

    db = SessionLocal()
    try:
        scenarios = db.scalars(select(Scenario).order_by(Scenario.id)).all()
        if not scenarios:
            raise RuntimeError("No scenarios were seeded.")

        results = []
        for scenario in scenarios:
            run = run_rule_based_agent(db, scenario)
            result = evaluate_run(db, run, scenario)
            if not result.passed:
                raise RuntimeError(f"Smoke test failed: {result.details}")
            results.append(result)

        print(
            {
                "scenarios": len(scenarios),
                "passed_runs": sum(1 for result in results if result.passed),
                "average_score": sum(result.score for result in results) / len(results),
                "average_tool_accuracy": (
                    sum(result.tool_accuracy for result in results) / len(results)
                ),
                "total_tool_calls_traced": sum(
                    result.total_tool_call_count for result in results
                ),
                "duplicate_usage_detected": sum(
                    result.duplicate_usage_quantity for result in results
                ),
                "overcharge_detected_dollars": sum(
                    result.detected_overcharge_cents for result in results
                )
                / 100,
                "passed": all(result.passed for result in results),
            }
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
