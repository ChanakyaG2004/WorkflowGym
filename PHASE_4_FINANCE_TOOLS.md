# WorkflowGym Phase 4: Deterministic Finance Tools

Phase 4 implements the tools the agent can call.

The implementation lives in:

```text
backend/app/tools/finance_tools.py
```

## Implemented Tools

The implemented tools are:

- `get_customer(customer_name)`
- `get_invoice(customer_id, month)`
- `get_usage_events(customer_id, month)`
- `get_contract_terms(customer_id)`
- `compare_usage_to_invoice(customer_id, month)`

Each tool is a normal Python function that receives a SQLAlchemy `Session`.

## Why These Tools Exist

The agent should not directly inspect every database table however it wants.

Instead, the simulator gives it a controlled tool interface. That is closer to how real tool-using AI agents work.

For the first version, these tools are deterministic. Given the same database state and input, they return the same output every time.

## Most Important Tool

`compare_usage_to_invoice` combines the other business facts:

- Valid usage
- Duplicate usage
- Contract included calls
- Invoice charged usage
- Correct overage
- Actual charged overage

It returns the key diagnosis fields:

```text
invoice_incorrect
cause
correct_billable_overage_calls
actual_charged_overage_calls
overcharge_cents
```

## What You Should Understand

- Tools are plain backend functions.
- Tools return structured dictionaries.
- The rule-based agent calls these same tools that a future LLM agent could call.
- Keeping tools deterministic makes evaluation easier.
- `compare_usage_to_invoice` is where the finance logic is concentrated.
