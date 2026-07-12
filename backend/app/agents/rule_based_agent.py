from datetime import datetime
from typing import Any, Callable

from sqlalchemy.orm import Session

from app.db.models import AgentRun, AgentStep, Scenario
from app.tools.finance_tools import (
    compare_usage_to_invoice,
    get_contract_terms,
    get_customer,
    get_invoice,
    get_usage_events,
)


ToolFn = Callable[..., dict[str, Any]]


def _record_tool_call(
    db: Session,
    run: AgentRun,
    step_number: int,
    tool_name: str,
    tool_fn: ToolFn,
    tool_input: dict[str, Any],
) -> dict[str, Any]:
    """Call a tool and store the input/output as an AgentStep."""
    tool_output = tool_fn(db, **tool_input)
    step = AgentStep(
        agent_run_id=run.id,
        step_number=step_number,
        tool_name=tool_name,
        tool_input=tool_input,
        tool_output=tool_output,
    )
    db.add(step)
    db.commit()
    return tool_output


def run_rule_based_agent(db: Session, scenario: Scenario) -> AgentRun:
    """Run a deterministic investigation for the duplicate usage scenario."""
    run = AgentRun(scenario_id=scenario.id, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)

    customer_result = _record_tool_call(
        db,
        run,
        1,
        "get_customer",
        get_customer,
        {"customer_name": scenario.customer_name},
    )
    customer_id = customer_result["customer"]["id"]

    _record_tool_call(
        db,
        run,
        2,
        "get_invoice",
        get_invoice,
        {"customer_id": customer_id, "month": scenario.month},
    )
    _record_tool_call(
        db,
        run,
        3,
        "get_usage_events",
        get_usage_events,
        {"customer_id": customer_id, "month": scenario.month},
    )
    _record_tool_call(
        db,
        run,
        4,
        "get_contract_terms",
        get_contract_terms,
        {"customer_id": customer_id},
    )
    comparison = _record_tool_call(
        db,
        run,
        5,
        "compare_usage_to_invoice",
        compare_usage_to_invoice,
        {"customer_id": customer_id, "month": scenario.month},
    )

    decision = "invoice_incorrect" if comparison["invoice_incorrect"] else "invoice_correct"
    final_answer = {
        "decision": decision,
        "cause": comparison["cause"],
        "explanation": (
            "The invoice charged overage on duplicate usage events. "
            f"Valid usage was {comparison['valid_usage_quantity']} API calls, "
            f"so billable overage should be {comparison['correct_billable_overage_calls']} calls. "
            f"The invoice charged {comparison['actual_charged_overage_calls']} overage calls."
        ),
        "evidence": [
            f"Valid usage quantity: {comparison['valid_usage_quantity']}",
            f"Duplicate usage quantity: {comparison['duplicate_usage_quantity']}",
            f"Correct billable overage calls: {comparison['correct_billable_overage_calls']}",
            f"Actual charged overage calls: {comparison['actual_charged_overage_calls']}",
            f"Overcharge cents: {comparison['overcharge_cents']}",
        ],
    }

    run.final_answer = final_answer
    run.status = "completed"
    run.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(run)
    return run
