from pydantic import BaseModel


class MetricsSummary(BaseModel):
    total_scenarios: int
    total_runs: int
    passed_runs: int
    pass_rate: float
    average_score: float
    average_tool_accuracy: float
    average_run_duration_ms: float
    total_tool_calls: int
    total_detected_overcharge_cents: int
    total_duplicate_usage_quantity: int
