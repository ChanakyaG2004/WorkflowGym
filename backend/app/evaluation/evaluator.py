from sqlalchemy.orm import Session

from app.db.models import AgentRun, EvaluationResult, Scenario


def evaluate_run(db: Session, run: AgentRun, scenario: Scenario) -> EvaluationResult:
    """Score a run against the scenario's hidden ground truth."""
    final_answer = run.final_answer or {}
    called_tools = {step.tool_name for step in run.steps}
    required_tools = set(scenario.required_tools)
    required_called = called_tools.intersection(required_tools)

    decision_correct = final_answer.get("decision") == scenario.expected_outcome
    cause_correct = final_answer.get("cause") == scenario.hidden_cause
    required_tool_count = len(required_tools)
    called_required_tool_count = len(required_called)
    missing_required_tool_count = required_tool_count - called_required_tool_count
    tool_accuracy = int((called_required_tool_count / required_tool_count) * 100)
    score = int(
        (int(decision_correct) * 40)
        + (int(cause_correct) * 40)
        + (tool_accuracy * 0.20)
    )
    passed = score == 100

    comparison = next(
        (
            step.tool_output
            for step in run.steps
            if step.tool_name == "compare_usage_to_invoice"
        ),
        {},
    )
    completed_at = run.completed_at or run.created_at
    run_duration_ms = int((completed_at - run.created_at).total_seconds() * 1000)

    result = EvaluationResult(
        agent_run_id=run.id,
        decision_correct=decision_correct,
        cause_correct=cause_correct,
        tool_accuracy=tool_accuracy,
        score=score,
        required_tool_count=required_tool_count,
        called_required_tool_count=called_required_tool_count,
        missing_required_tool_count=missing_required_tool_count,
        total_tool_call_count=len(run.steps),
        run_duration_ms=run_duration_ms,
        detected_overcharge_cents=comparison.get("overcharge_cents", 0),
        duplicate_usage_quantity=comparison.get("duplicate_usage_quantity", 0),
        passed=passed,
        details={
            "expected_outcome": scenario.expected_outcome,
            "actual_decision": final_answer.get("decision"),
            "hidden_cause": scenario.hidden_cause,
            "actual_cause": final_answer.get("cause"),
            "score_breakdown": {
                "decision_correct_points": 40 if decision_correct else 0,
                "cause_correct_points": 40 if cause_correct else 0,
                "tool_accuracy_points": int(tool_accuracy * 0.20),
            },
            "required_tools": sorted(required_tools),
            "called_tools": sorted(called_tools),
            "missing_tools": sorted(required_tools - called_tools),
            "overcharge_dollars": comparison.get("overcharge_cents", 0) / 100,
        },
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
