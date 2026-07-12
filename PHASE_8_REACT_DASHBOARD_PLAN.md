# WorkflowGym Phase 8: React Dashboard Plan

Phase 8 is not implemented yet.

The backend milestone is complete first so the frontend will have real API endpoints to call.

## Dashboard Goal

The React dashboard should make WorkflowGym understandable visually.

It should show:

- Available scenarios
- A button to run a scenario
- Agent runs
- Tool-call traces
- Final answers
- Evaluation results

## First Useful Screens

### Scenario List

Shows available scenarios from:

```text
GET /scenarios
```

For the MVP, this will show:

```text
duplicate_usage_001
```

### Run Detail

Shows one run from:

```text
GET /runs/{run_id}
```

This should display:

- Scenario
- Final decision
- Final cause
- Evidence
- Evaluation pass/fail
- Tool accuracy
- Ordered tool trace

### Runs List

Shows previous runs from:

```text
GET /runs
```

## Suggested Frontend Stack

Use:

- React
- TypeScript
- Vite
- Fetch API or TanStack Query

Avoid adding authentication, complex state management, or charts at first.

## What To Build First

The first dashboard version should be simple:

1. Load scenarios.
2. Let the user run `duplicate_usage_001`.
3. Show the returned trace and evaluation.

That is enough to demonstrate the project in a resume walkthrough.

## What You Should Understand

- The frontend should visualize the backend workflow, not replace it.
- The trace is the most important UI artifact.
- Evaluation results should be easy to inspect.
- The dashboard should help someone understand how the agent reached its answer.
