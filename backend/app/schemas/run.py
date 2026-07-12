from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AgentStepRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    step_number: int
    tool_name: str
    tool_input: dict[str, Any]
    tool_output: dict[str, Any]
    created_at: datetime


class EvaluationResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    decision_correct: bool
    cause_correct: bool
    tool_accuracy: int
    score: int
    required_tool_count: int
    called_required_tool_count: int
    missing_required_tool_count: int
    total_tool_call_count: int
    run_duration_ms: int
    detected_overcharge_cents: int
    duplicate_usage_quantity: int
    passed: bool
    details: dict[str, Any]


class AgentRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scenario_id: int
    status: str
    final_answer: dict[str, Any] | None
    created_at: datetime
    completed_at: datetime | None
    steps: list[AgentStepRead]
    evaluation_result: EvaluationResultRead | None
