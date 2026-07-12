# WorkflowGym

**Live Demo:** https://workflowgym.vercel.app  
**API Docs:** https://workflowgym.vercel.app/docs  
**Raw Demo JSON:** https://workflowgym.vercel.app/api/demo

WorkflowGym is a deployable benchmark for testing tool-using AI agents in simulated FinanceOps workflows.

The current MVP is a backend-first FinanceOps simulator. A rule-based agent investigates 20 seeded invoice scenarios, calls deterministic finance tools, stores tool-call traces, and gets evaluated against hidden ground truth.

Current benchmark results:

- 20/20 passing runs
- 100% pass rate
- 100/100 average evaluator score
- 100% average tool accuracy
- 100 traced tool calls
- 145,000 duplicate API calls detected
- $29,600 total overcharge identified

## Highlights

WorkflowGym demonstrates:

- FastAPI backend architecture
- PostgreSQL persistence with SQLAlchemy ORM
- Deterministic tool interface for agent workflows
- Trace storage for every tool call
- Hidden-ground-truth evaluation
- Quantified evaluation metrics: score, pass rate, tool accuracy, tool-call count, run duration, duplicate usage detected, and overcharge detected
- Dockerized local deployment
- Human-friendly live demo UI

## Benchmark Scenarios

```text
duplicate_usage_001
duplicate_usage_002
duplicate_usage_003
duplicate_usage_004
overage_rate_mismatch_001
overage_rate_mismatch_002
overage_rate_mismatch_003
overage_rate_mismatch_004
included_allowance_not_applied_001
included_allowance_not_applied_002
included_allowance_not_applied_003
below_allowance_overage_001
below_allowance_overage_002
below_allowance_overage_003
invoice_usage_exceeds_records_001
invoice_usage_exceeds_records_002
invoice_usage_exceeds_records_003
invoice_correct_001
invoice_correct_002
invoice_correct_003
```

The benchmark covers:

- duplicate usage events
- overage rate mismatch
- included allowance not applied
- below-allowance overage charge
- invoice usage exceeding recorded usage
- a correct-invoice control case

## Data Provenance

The current 20 benchmark scenarios use a **real public pricing reference plus synthetic benchmark invoices**.

Real public source:

- AWS API Gateway pricing: https://aws.amazon.com/api-gateway/pricing/

Real facts used as benchmark context:

- API Gateway charges for API calls received and data transferred out.
- AWS REST API pricing examples use `$3.50 per million API calls`.
- AWS API Gateway pricing examples use `$0.09 per GB` for data transfer.

Synthetic parts:

- customer names
- usage volumes
- invoice line items
- injected billing errors
- hidden ground truth labels

Why synthetic data:

- Real customer invoices and usage logs are usually private.
- Hidden ground truth needs to be controlled so the evaluator can score runs deterministically.
- Synthetic fixtures let the benchmark safely test known billing failure modes.

Additional public real-world sources that could be integrated in a future version:

- SEC EDGAR APIs for public company filings and financial facts: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- AWS Price List Bulk API for public cloud pricing data: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-the-aws-price-list-bulk-api.html

In the live UI, each scenario is labeled with its data source type.

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
GET  /api/demo
```

Local interactive API docs are available at:

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
scenarios: 20
passed_runs: 20
average_score: 100.0
average_tool_accuracy: 100.0
total_tool_calls_traced: 100
duplicate_usage_detected: 145000
overcharge_detected_dollars: 29600.0
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
  "total_scenarios": 20,
  "total_runs": 20,
  "passed_runs": 20,
  "pass_rate": 100.0,
  "average_score": 100.0,
  "average_tool_accuracy": 100.0,
  "total_tool_calls": 100,
  "total_detected_overcharge_cents": 2960000,
  "total_duplicate_usage_quantity": 145000
}
```

## Deployment

The API is containerized with [backend/Dockerfile](backend/Dockerfile). A Render Blueprint is available in [render.yaml](render.yaml) for a PostgreSQL-backed deployment.

The live Vercel demo uses [vercel.json](vercel.json) and [api/index.py](api/index.py) with SQLite in `/tmp`, so `/demo` runs the full benchmark in one request for stateless hosting.

For raw serverless demo JSON, use:

```text
https://workflowgym.vercel.app/api/demo
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

## Resume Bullets

```text
WorkflowGym | Tool-Using AI Agent Evaluation Platform | Python, FastAPI, SQLAlchemy, Docker, Vercel | GitHub | Live Demo
Built a FastAPI backend for evaluating tool-using AI agents across 20 simulated FinanceOps billing scenarios with hidden ground truth, deterministic tools, trace storage, and automated scoring.
Implemented 5 finance tools covering customer lookup, invoice inspection, usage analysis, contract terms, and invoice-vs-usage comparison, storing 100 total tool calls as auditable traces.
Achieved 20/20 passing benchmark runs with 100% pass rate, 100/100 average evaluator score, 100% tool accuracy, 145,000 duplicate API calls detected, and $29,600 total overcharge identified.
```
