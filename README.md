# WorkflowGym

WorkflowGym is a full-stack project foundation for testing tool-using AI agents in simulated business workflows.

The current MVP is a backend-first FinanceOps simulator. A rule-based agent investigates six seeded invoice scenarios, calls deterministic finance tools, stores tool-call traces, and gets evaluated against hidden ground truth.

## Resume Summary

WorkflowGym demonstrates:

- FastAPI backend architecture
- PostgreSQL persistence with SQLAlchemy ORM
- Deterministic tool interface for agent workflows
- Trace storage for every tool call
- Hidden-ground-truth evaluation
- Quantified evaluation metrics: score, pass rate, tool accuracy, tool-call count, run duration, duplicate usage detected, and overcharge detected
- Dockerized local deployment
- API-first design ready for a future React dashboard

## Current Scenarios

```text
duplicate_usage_001
overage_rate_mismatch_001
included_allowance_not_applied_001
below_allowance_overage_001
invoice_usage_exceeds_records_001
invoice_correct_001
```

The benchmark covers:

- duplicate usage events
- overage rate mismatch
- included allowance not applied
- below-allowance overage charge
- invoice usage exceeding recorded usage
- a correct-invoice control case

## Architecture

```text
backend/app/
  main.py                  FastAPI app and API routes
  db/
    database.py            SQLAlchemy engine/session setup
    models.py              ORM models
    init_db.py             create_all helper
  seed/
    seed_acme.py           Acme AI seed data
  tools/
    finance_tools.py       deterministic finance tools
  agents/
    rule_based_agent.py    first deterministic agent runner
  evaluation/
    evaluator.py           hidden-ground-truth evaluator
  schemas/
    scenario.py            scenario response schema
    run.py                 run/trace/evaluation response schemas
```

## API Endpoints

```text
GET  /health
GET  /scenarios
POST /scenarios/{scenario_id}/run
GET  /runs
GET  /runs/{run_id}
GET  /metrics/summary
GET  /demo
```

Live demo:

```text
https://workflowgym.vercel.app
```

Interactive API docs are available at:

```text
http://127.0.0.1:8000/docs
```

## Run With Docker Compose

From the project root:

```bash
docker compose up --build
```

In another terminal, seed the demo data:

```bash
docker compose exec api python -m app.seed.seed_acme
```

Run the scenario:

```bash
curl -X POST http://127.0.0.1:8000/scenarios/duplicate_usage_001/run
```

Fetch all runs:

```bash
curl http://127.0.0.1:8000/runs
```

## Local Development

From `backend/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set up PostgreSQL so this URL works:

```text
postgresql+psycopg://workflowgym:workflowgym@localhost:5432/workflowgym
```

Then run:

```bash
python -m app.seed.seed_acme
uvicorn app.main:app --reload
```

## Smoke Test

The smoke test seeds all demo scenarios, runs the benchmark, evaluates every run, and fails if any expected result is not produced.

With Docker Compose:

```bash
docker compose exec api python -m app.scripts.smoke_test
```

Locally from `backend/`:

```bash
python -m app.scripts.smoke_test
```

Expected result:

```text
passed: True
scenarios: 6
passed_runs: 6
average_score: 100.0
average_tool_accuracy: 100.0
total_tool_calls_traced: 30
duplicate_usage_detected: 50000
overcharge_detected_dollars: 9600.0
```

## Tests

Install dev dependencies:

```bash
cd backend
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Run the test suite:

```bash
DATABASE_URL=sqlite+pysqlite:////tmp/workflowgym_pytest.db pytest -q
```

The tests validate:

- duplicate usage and overcharge detection
- agent trace storage
- evaluator scoring metrics
- aggregate metrics summary

## Quantifiable Metrics

Each evaluated run stores:

- `score`: 0-100 weighted score
- `tool_accuracy`: percent of required tools called
- `required_tool_count`
- `called_required_tool_count`
- `missing_required_tool_count`
- `total_tool_call_count`
- `run_duration_ms`
- `detected_overcharge_cents`
- `duplicate_usage_quantity`

The aggregate endpoint summarizes portfolio-friendly metrics:

```text
GET /metrics/summary
```

Example metrics after one full benchmark run:

```json
{
  "total_scenarios": 6,
  "total_runs": 6,
  "passed_runs": 6,
  "pass_rate": 100.0,
  "average_score": 100.0,
  "average_tool_accuracy": 100.0,
  "total_tool_calls": 30,
  "total_detected_overcharge_cents": 960000,
  "total_duplicate_usage_quantity": 50000
}
```

## Deployment Notes

The API is containerized with [backend/Dockerfile](backend/Dockerfile). A Render Blueprint is available in [render.yaml](render.yaml).

The root [Dockerfile](Dockerfile) is a lightweight public-demo container for Hugging Face Spaces. It runs the same API with SQLite and auto-seeded data.

The [vercel.json](vercel.json) and [api/index.py](api/index.py) files support a lightweight Vercel demo with SQLite in `/tmp`.

For raw serverless demo JSON, use:

```text
https://workflowgym.vercel.app/demo
```

That endpoint seeds, runs, evaluates, and returns metrics in one request.

For a hosted deployment, provide:

```text
DATABASE_URL
PORT
AUTO_SEED_DEMO
```

The app creates tables on startup using SQLAlchemy `create_all` for the learning MVP. A production version should replace that with Alembic migrations.

Set `AUTO_SEED_DEMO=true` on a demo deployment to seed the benchmark scenarios when they are missing.

## Next Milestones

- Add Alembic migrations.
- Add React + TypeScript dashboard.
- Add an LLM-powered agent that calls the same deterministic tools.
- Add more business workflow scenarios.
