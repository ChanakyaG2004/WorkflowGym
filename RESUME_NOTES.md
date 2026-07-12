# Resume Notes

## Project Title

WorkflowGym: Tool-Using AI Agent Evaluation Platform

GitHub: https://github.com/ChanakyaG2004/WorkflowGym

Live demo: https://workflowgym.vercel.app

Raw API demo: https://workflowgym.vercel.app/demo

## Short Description

Built a FastAPI and PostgreSQL backend for evaluating tool-using AI agents in simulated FinanceOps workflows. The MVP seeds six billing scenarios, runs a deterministic agent through finance tools, stores every tool call as a trace, and evaluates final answers against hidden ground truth.

## Resume Bullets

- Built a Dockerized FastAPI backend for a FinanceOps agent-evaluation simulator using PostgreSQL, SQLAlchemy, and Pydantic, with a repeatable 1-command smoke test.
- Modeled 9 core entities covering customer billing data, invoices, usage events, scenarios, agent runs, tool-call traces, and evaluation results with SQLAlchemy ORM.
- Implemented 5 deterministic finance tools across 6 seeded FinanceOps scenarios covering duplicate usage, rate mismatch, missing allowance, below-allowance overage, usage-record mismatch, and a correct-invoice control case.
- Created a rule-based agent runner that stores 100% of tool invocations as auditable `AgentStep` traces, producing 30 traced tool calls across the benchmark.
- Built an evaluator that achieved 6/6 passing runs, 100% pass rate, 100/100 average score, 100% average tool accuracy, 50,000 duplicate API calls detected, and $9,600 total overcharge identified.
- Added seed data, Docker Compose, API docs, and a smoke test for repeatable local demos.

## Interview Demo Script

1. Explain that WorkflowGym evaluates tool-using agents, not just final answers.
2. Open the live UI and run the six-scenario benchmark.
3. Show the aggregate metrics: 6 scenarios, 6/6 passed, 100% pass rate, 100 average score, and 30 tool calls traced.
4. Walk through the scenario results and causes.
5. Open `/docs` and show the backend API.
6. Open `/demo` and show the raw JSON metrics.
7. Explain how a future LLM agent can call the same deterministic tools.
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
