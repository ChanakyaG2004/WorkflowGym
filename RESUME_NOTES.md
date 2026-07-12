# Resume Notes

## Project Title

WorkflowGym: Tool-Using AI Agent Evaluation Platform

## Short Description

Built a FastAPI and PostgreSQL backend for evaluating tool-using AI agents in simulated FinanceOps workflows. The MVP seeds a duplicate billing scenario, runs a deterministic agent through finance tools, stores every tool call as a trace, and evaluates the final answer against hidden ground truth.

## Resume Bullets

- Built a Dockerized FastAPI backend for a FinanceOps agent-evaluation simulator using PostgreSQL, SQLAlchemy, and Pydantic, with a repeatable 1-command smoke test.
- Modeled 9 core entities covering customer billing data, invoices, usage events, scenarios, agent runs, tool-call traces, and evaluation results with SQLAlchemy ORM.
- Implemented 5 deterministic finance tools that let an agent inspect customers, invoices, usage, contract terms, and invoice correctness.
- Created a rule-based agent runner that stores 100% of tool invocations as auditable `AgentStep` traces before producing a structured final answer.
- Built an evaluator that computes a 0-100 score, pass/fail, tool accuracy, run duration, required-tool coverage, duplicate usage detected, and overcharge detected for each run.
- Added seed data, Docker Compose, API docs, and a smoke test for repeatable local demos.

## Interview Demo Script

1. Explain that WorkflowGym evaluates tool-using agents, not just final answers.
2. Show the seeded `duplicate_usage_001` scenario.
3. Run `POST /scenarios/duplicate_usage_001/run`.
4. Open the returned run.
5. Walk through the five stored tool calls.
6. Show the final answer and evaluation result: score 100, 5/5 required tools called, 50,000 duplicate API calls detected, and $2,000 overcharge detected.
7. Open `/metrics/summary` and show aggregate pass rate, average score, average tool accuracy, and total tool calls.
8. Explain how a future LLM agent can call the same deterministic tools.

## Current Technical Scope

- Backend: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Schemas: Pydantic
- Deployment: Docker and Docker Compose
- Agent: deterministic rule-based runner
- LLM integration: intentionally deferred
- Frontend: planned React + TypeScript dashboard
