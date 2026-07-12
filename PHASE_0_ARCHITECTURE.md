# WorkflowGym Phase 0: Architecture

WorkflowGym is a backend-first simulation platform for testing tool-using AI agents in business workflows.

The first MVP is a FinanceOps simulator. An agent investigates a billing issue, calls deterministic tools, leaves a trace of every step, and is evaluated against hidden ground truth.

For now, there is no frontend, no LLM integration, no LangGraph, no authentication, and no Docker. The first goal is to understand the backend architecture clearly before adding more moving parts.

## What We Are Building

The first backend milestone will simulate one billing investigation:

- Customer: Acme AI
- Scenario: `duplicate_usage_001`
- Complaint: Acme AI says its June 2026 invoice is too high
- Hidden cause: duplicate usage events
- Expected result: the agent should conclude that the invoice is incorrect

The backend will support this flow:

1. Seed fake FinanceOps data into PostgreSQL.
2. Load a scenario with hidden ground truth.
3. Run a rule-based agent.
4. Let the agent call deterministic finance tools.
5. Store every tool call as an agent trace.
6. Evaluate the agent's final answer.
7. Return run and evaluation results through API endpoints.

## Why This Architecture Exists

WorkflowGym is not just a CRUD app. It is an evaluation harness.

That means the system needs to track more than the final answer. It needs to know:

- What task the agent was trying to solve.
- Which tools the agent called.
- What each tool returned.
- Whether the final answer matched hidden ground truth.
- Whether the agent used the required evidence-gathering steps.

This is why the project has separate concepts for scenarios, agent runs, agent steps, tools, and evaluation results.

## Main Backend Layers

The backend will be split into four main layers.

```text
API layer
FastAPI routes such as /health, /scenarios, and /runs

Application layer
Scenario execution, rule-based agent runner, and evaluator

Tool layer
Deterministic finance tools like get_invoice and compare_usage_to_invoice

Data layer
SQLAlchemy models, database session setup, and seed data
```

This separation matters because later we can replace the rule-based agent with an LLM-powered agent while keeping the same tools, traces, and evaluator.

## Proposed Folder Structure

```text
WorkflowGym/
  backend/
    app/
      __init__.py
      main.py

      db/
        __init__.py
        database.py
        models.py

      schemas/
        __init__.py
        scenario.py
        run.py

      tools/
        __init__.py
        finance_tools.py

      agents/
        __init__.py
        rule_based_agent.py

      evaluation/
        __init__.py
        evaluator.py

      seed/
        __init__.py
        seed_acme.py

    requirements.txt
```

The exact structure may change slightly as the code grows, but this is the shape we are aiming for.

## Folder Responsibilities

### `backend/app/main.py`

Creates the FastAPI app and registers API routes.

In Phase 1, this will expose a simple `/health` endpoint so we can confirm the backend starts correctly.

### `backend/app/db/database.py`

Owns the database connection setup:

- PostgreSQL database URL
- SQLAlchemy engine
- Session factory
- Declarative base class for models

This file is infrastructure. Other parts of the app should use it instead of creating database connections directly.

### `backend/app/db/models.py`

Defines the database tables using SQLAlchemy ORM models.

The main models will be:

- `Customer`
- `PricingPlan`
- `UsageEvent`
- `Invoice`
- `InvoiceLineItem`
- `Scenario`
- `AgentRun`
- `AgentStep`
- `EvaluationResult`

These models represent both the FinanceOps business data and the agent evaluation data.

### `backend/app/schemas/`

Contains Pydantic schemas.

Schemas define the shape of structured data moving in and out of the API. They are also useful for making the agent's final answer explicit.

For example, the agent will eventually produce something like:

```json
{
  "decision": "invoice_incorrect",
  "cause": "duplicate_usage_events",
  "explanation": "The invoice charged 100,000 overage calls, but only 50,000 should have been billable.",
  "evidence": []
}
```

### `backend/app/tools/finance_tools.py`

Contains deterministic tools the agent can call.

Examples:

- `get_customer(customer_name)`
- `get_invoice(customer_id, month)`
- `get_usage_events(customer_id, month)`
- `get_contract_terms(customer_id)`
- `compare_usage_to_invoice(customer_id, month)`

These are normal Python functions. They are not LLM tools yet. Starting with deterministic functions makes the system easier to test and understand.

### `backend/app/agents/rule_based_agent.py`

Contains the first simple agent runner.

This agent will not use an LLM. It will follow a fixed investigation sequence:

1. Look up the customer.
2. Load the invoice.
3. Load usage events.
4. Load contract terms.
5. Compare usage to invoice.
6. Produce a structured final answer.

The point is to prove the workflow works before introducing an LLM.

### `backend/app/evaluation/evaluator.py`

Compares the agent's final answer to the scenario's hidden ground truth.

The evaluator will check:

- Did the final decision match the expected outcome?
- Did the cause match the hidden cause?
- Did the agent call the required tools?

It will then store an `EvaluationResult`.

### `backend/app/seed/seed_acme.py`

Creates the first fake dataset.

This seed script will insert:

- Acme AI as a customer
- A pricing plan with 100,000 included API calls
- June 2026 usage events
- A duplicated usage problem
- An incorrect invoice
- The `duplicate_usage_001` scenario

Seed data gives us a stable sandbox where the answer is known ahead of time.

## Core Data Flow

Eventually, running a scenario will look like this:

```text
POST /scenarios/duplicate_usage_001/run
        |
        v
Load Scenario
        |
        v
Create AgentRun
        |
        v
Rule-based agent calls tools
        |
        v
Each tool call creates AgentStep
        |
        v
Agent returns final answer
        |
        v
Evaluator checks answer against hidden ground truth
        |
        v
Store EvaluationResult
        |
        v
Return run summary
```

## Important Domain Concepts

### Scenario

A scenario is the task the agent must solve.

For this milestone, the scenario is:

```text
duplicate_usage_001
```

It includes visible information, such as the customer's complaint, and hidden information, such as the correct cause and expected outcome.

### AgentRun

An `AgentRun` represents one attempt to solve a scenario.

If you run the same scenario five times, you should get five `AgentRun` records.

### AgentStep

An `AgentStep` records one tool call made during an agent run.

It should store information like:

- Tool name
- Tool input
- Tool output
- Step order

This is what creates the trace.

### EvaluationResult

An `EvaluationResult` stores the score or judgment for a run.

For the first version, the evaluation will be simple and deterministic:

- Did the decision match?
- Did the cause match?
- What fraction of required tools were called?

## First Milestone Learning Objective

By the end of the backend-only milestone, you should understand how to build a small but real evaluation harness for tool-using agents.

Specifically, you should understand:

- How FastAPI exposes backend workflows as API endpoints.
- How SQLAlchemy models represent business entities and agent traces.
- How PostgreSQL stores both domain data and evaluation data.
- How deterministic tools create a controlled environment for agents.
- How an agent run can be traced step by step.
- How hidden ground truth enables automatic evaluation.
- Why separating tools, agent logic, and evaluator logic matters.

## What You Should Understand Before Moving On

Before starting Phase 1, make sure these ideas are clear:

- A `Scenario` defines the task and hidden expected answer.
- An `AgentRun` represents one attempt to solve a scenario.
- An `AgentStep` records each tool call the agent made.
- Tools are plain backend functions, not LLM magic.
- The evaluator checks the agent's final answer against hidden ground truth.
- We are starting with `create_all`, not Alembic, so the database setup stays easy to understand.

Once this architecture makes sense, the next step is Phase 1: set up FastAPI, SQLAlchemy, the PostgreSQL connection, and a `/health` endpoint.

## Implementation Status

The backend milestone has now been implemented through Phase 7.

The implemented backend includes:

- SQLAlchemy models in `backend/app/db/models.py`
- Acme AI seed script in `backend/app/seed/seed_acme.py`
- Deterministic finance tools in `backend/app/tools/finance_tools.py`
- Rule-based agent runner in `backend/app/agents/rule_based_agent.py`
- Evaluator in `backend/app/evaluation/evaluator.py`
- API endpoints in `backend/app/main.py`

Phase 8 remains a planning phase for the future React dashboard. No frontend has been added yet.
