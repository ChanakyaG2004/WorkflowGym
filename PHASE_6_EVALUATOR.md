# WorkflowGym Phase 6: Evaluator

Phase 6 implements automatic scoring.

The implementation lives in:

```text
backend/app/evaluation/evaluator.py
```

## What The Evaluator Checks

The evaluator compares the agent run to the scenario's hidden ground truth.

It checks:

- Did the final decision match `expected_outcome`?
- Did the final cause match `hidden_cause`?
- Did the agent call all required tools?
- How many tool calls were traced?
- How long did the run take?
- How much duplicate usage and overcharge did the agent identify?

## Tool Accuracy

Tool accuracy is calculated as:

```text
required tools called / total required tools
```

The implementation stores it as an integer percentage.

For the Acme scenario, the correct tool accuracy is:

```text
100
```

because the rule-based agent calls all five required tools.

## Stored Result

The evaluator stores an `EvaluationResult` with:

- `decision_correct`
- `cause_correct`
- `tool_accuracy`
- `score`
- `required_tool_count`
- `called_required_tool_count`
- `missing_required_tool_count`
- `total_tool_call_count`
- `run_duration_ms`
- `detected_overcharge_cents`
- `duplicate_usage_quantity`
- `passed`
- `details`

## What You Should Understand

- The agent does not grade itself.
- Hidden ground truth stays on the scenario.
- The evaluator produces a separate durable result.
- A run can have the right final answer but still have weak tool usage in future versions.
