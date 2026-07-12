# WorkflowGym Phase 3: Seed Data

Phase 3 creates the first complete FinanceOps scenario dataset.

The implementation lives in:

```text
backend/app/seed/seed_acme.py
```

## What It Seeds

The seed script creates one customer:

```text
Acme AI
```

It creates a pricing plan:

```text
100,000 included API calls
4 cents per extra API call
```

It creates June 2026 usage:

```text
150,000 valid API calls
50,000 duplicate API calls
```

It creates an incorrect invoice:

```text
Invoice usage quantity: 200,000 API calls
Correct billable overage: 50,000 calls
Actual charged overage: 100,000 calls
Invoice overcharge cause: duplicate usage events
```

It also creates the scenario:

```text
duplicate_usage_001
```

## Why This Exists

The seed script gives the simulator stable known data.

That matters because the evaluator needs hidden ground truth. We know the correct answer before the agent runs:

```text
expected_outcome = invoice_incorrect
hidden_cause = duplicate_usage_events
```

## How To Run It

From `backend/`:

```bash
source .venv/bin/activate
python -m app.seed.seed_acme
```

PostgreSQL must be running and the configured database must exist.

## Important Detail

The seed script clears existing WorkflowGym rows before reseeding. That makes it easy to rerun while learning.

This is useful for development, but a production seed script would usually be more careful.

## What You Should Understand

- Seed data makes the simulator repeatable.
- The visible task is the customer's complaint.
- The hidden ground truth lives on the `Scenario`.
- The invoice is intentionally wrong.
- The duplicate usage event is the hidden cause the agent must discover.
