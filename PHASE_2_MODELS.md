# WorkflowGym Phase 2: Database Models

Phase 2 is where WorkflowGym gets its core data model.

In Phase 1, we created the FastAPI app and the SQLAlchemy database connection. In Phase 2, we will define the database tables that represent the FinanceOps world, the scenario system, the agent trace, and the evaluation result.

We are still not building the full app yet. This phase is about understanding the shape of the data.

## What We Are Building

We will create SQLAlchemy ORM models for:

- `Customer`
- `PricingPlan`
- `UsageEvent`
- `Invoice`
- `InvoiceLineItem`
- `Scenario`
- `AgentRun`
- `AgentStep`
- `EvaluationResult`

These models will live in:

```text
backend/app/db/models.py
```

We will also use the `Base` class from:

```text
backend/app/db/database.py
```

Every model class will inherit from `Base` so SQLAlchemy knows how to map it to a database table.

## Why These Models Exist

WorkflowGym has two kinds of data:

1. Business workflow data
2. Agent evaluation data

The business workflow data represents the fake FinanceOps system:

- Who the customer is
- What pricing plan they are on
- What usage they had
- What invoice they received
- What line items appeared on the invoice

The agent evaluation data represents the simulator:

- What scenario the agent was solving
- What run was created
- What tools the agent called
- What final answer the agent gave
- Whether the answer was correct

This split matters because WorkflowGym is not only storing invoices. It is storing evidence about how an agent investigated those invoices.

## Business Data Models

### Customer

Represents a company using the product.

For the MVP, we will seed one customer:

```text
Acme AI
```

Important fields:

- `id`
- `name`

Relationships:

- One customer can have one or more pricing plans.
- One customer can have many usage events.
- One customer can have many invoices.

### PricingPlan

Represents the customer's contract terms.

For Acme AI:

```text
100,000 included API calls
$0.04 per extra API call
```

Important fields:

- `id`
- `customer_id`
- `included_api_calls`
- `overage_rate_cents`

Why store cents instead of dollars?

Money should usually be stored as integer cents instead of floating-point dollars. For example, `$0.04` becomes `4` cents. This avoids rounding problems.

Relationships:

- A pricing plan belongs to one customer.

### UsageEvent

Represents usage recorded by the system.

For this MVP, we do not need to store every individual API call. Instead, each `UsageEvent` can represent a batch of usage.

Example:

```text
150,000 valid API calls for June 2026
50,000 duplicate API calls for June 2026
```

Important fields:

- `id`
- `customer_id`
- `month`
- `event_type`
- `quantity`
- `is_duplicate`

Relationships:

- A usage event belongs to one customer.

### Invoice

Represents the invoice sent to the customer.

For the scenario:

```text
Acme AI's June 2026 invoice charged for 200,000 total API calls.
```

Important fields:

- `id`
- `customer_id`
- `month`
- `total_cents`

Relationships:

- An invoice belongs to one customer.
- An invoice has many invoice line items.

### InvoiceLineItem

Represents a single charge on an invoice.

For example:

```text
API call overage: 100,000 calls at $0.04 each
```

Important fields:

- `id`
- `invoice_id`
- `description`
- `quantity`
- `unit_price_cents`
- `amount_cents`

Relationships:

- An invoice line item belongs to one invoice.

## Scenario And Evaluation Models

### Scenario

Represents a task that an agent must solve.

For the MVP:

```text
duplicate_usage_001
```

The visible part of the scenario is the customer's complaint:

```text
Acme AI says its June 2026 invoice is too high.
```

The hidden part is the ground truth:

```text
expected_outcome = invoice_incorrect
hidden_cause = duplicate_usage_events
```

Important fields:

- `id`
- `scenario_key`
- `customer_name`
- `month`
- `prompt`
- `expected_outcome`
- `hidden_cause`
- `required_tools`

Why store `required_tools`?

The evaluator will use it to check whether the agent called the tools needed to investigate the issue.

Relationships:

- A scenario can have many agent runs.

### AgentRun

Represents one attempt to solve a scenario.

If the same scenario is run ten times, there should be ten `AgentRun` records.

Important fields:

- `id`
- `scenario_id`
- `status`
- `final_answer`

Relationships:

- An agent run belongs to one scenario.
- An agent run has many agent steps.
- An agent run has one evaluation result.

### AgentStep

Represents one tool call made by the agent.

This is one of the most important tables in WorkflowGym because it creates the trace.

Example steps:

```text
1. get_customer({"customer_name": "Acme AI"})
2. get_invoice({"customer_id": 1, "month": "2026-06"})
3. get_usage_events({"customer_id": 1, "month": "2026-06"})
4. get_contract_terms({"customer_id": 1})
5. compare_usage_to_invoice({"customer_id": 1, "month": "2026-06"})
```

Important fields:

- `id`
- `agent_run_id`
- `step_number`
- `tool_name`
- `tool_input`
- `tool_output`

Relationships:

- An agent step belongs to one agent run.

### EvaluationResult

Stores the evaluator's judgment for one agent run.

Important fields:

- `id`
- `agent_run_id`
- `decision_correct`
- `cause_correct`
- `tool_accuracy`
- `passed`

Relationships:

- An evaluation result belongs to one agent run.

## Relationship Map

Here is the conceptual relationship map:

```text
Customer
  |
  |-- PricingPlan
  |
  |-- UsageEvent
  |
  |-- Invoice
        |
        |-- InvoiceLineItem

Scenario
  |
  |-- AgentRun
        |
        |-- AgentStep
        |
        |-- EvaluationResult
```

The `Customer` side represents the fake FinanceOps data.

The `Scenario` side represents the simulator and evaluation system.

## Why Relationships Matter

SQLAlchemy relationships let us move between connected records in Python.

For example:

```python
invoice.customer
```

can give us the customer for an invoice.

```python
invoice.line_items
```

can give us all line items for that invoice.

```python
agent_run.steps
```

can give us the full trace for a run.

Relationships make the code easier to read because we can work with connected Python objects instead of manually writing joins everywhere.

## JSON Fields

Some fields are naturally structured and flexible:

- `Scenario.required_tools`
- `AgentRun.final_answer`
- `AgentStep.tool_input`
- `AgentStep.tool_output`

For the first version, these can be stored as SQLAlchemy `JSON` columns.

That keeps the schema simple while still letting us store structured data.

Example `final_answer`:

```json
{
  "decision": "invoice_incorrect",
  "cause": "duplicate_usage_events",
  "explanation": "The invoice charged duplicate usage events.",
  "evidence": [
    "Valid usage was 150,000 API calls.",
    "Invoice charged overage on 200,000 total calls."
  ]
}
```

## What We Are Not Doing Yet

In Phase 2, we are not yet:

- Seeding Acme AI data
- Building finance tools
- Running the agent
- Evaluating the result
- Creating API endpoints beyond `/health`
- Adding Alembic migrations

We are only defining the database tables and relationships.

## Why No Alembic Yet

Alembic is the standard migration tool for SQLAlchemy projects.

However, for the first learning version, we will use:

```python
Base.metadata.create_all(bind=engine)
```

This directly creates tables from the SQLAlchemy models.

That is not how a mature production app should manage schema changes, but it is useful while learning because it makes the connection between model classes and database tables very direct.

We can add Alembic later once the basic model design is clear.

## Exact Learning Objective

By the end of Phase 2, you should understand:

- What each table represents.
- Which tables model FinanceOps data.
- Which tables model agent evaluation data.
- How SQLAlchemy models map Python classes to database tables.
- Why foreign keys connect related records.
- Why relationships make ORM code easier to navigate.
- Why agent traces need their own table.
- Why hidden ground truth belongs on the scenario, not the agent run.

## What You Should Understand Before Moving On

Before Phase 3, make sure these ideas are clear:

- `Customer`, `PricingPlan`, `UsageEvent`, `Invoice`, and `InvoiceLineItem` describe the fake business system.
- `Scenario`, `AgentRun`, `AgentStep`, and `EvaluationResult` describe the simulation and evaluation system.
- `AgentStep` is what lets us inspect the agent's reasoning path.
- `Scenario` stores hidden ground truth.
- `AgentRun` stores one attempt.
- `EvaluationResult` stores the judgment of that attempt.
- JSON columns are useful for flexible structured fields like tool input and output.
- `create_all` is a simple learning-friendly alternative to migrations for now.

Once this model design makes sense, the next step is to write the actual SQLAlchemy model code in `backend/app/db/models.py`.

## Implementation Status

Phase 2 is implemented in:

```text
backend/app/db/models.py
```

The implemented models are:

- `Customer`
- `PricingPlan`
- `UsageEvent`
- `Invoice`
- `InvoiceLineItem`
- `Scenario`
- `AgentRun`
- `AgentStep`
- `EvaluationResult`

The simple `create_all` helper is implemented in:

```text
backend/app/db/init_db.py
```

That helper imports the models and calls:

```python
Base.metadata.create_all(bind=engine)
```

This keeps the first version migration-free while you learn how SQLAlchemy model classes become database tables.
