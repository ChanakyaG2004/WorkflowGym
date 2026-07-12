# WorkflowGym

**Live Demo:** https://workflowgym.vercel.app  
**API Docs:** https://workflowgym.vercel.app/docs  
**Raw Demo JSON:** https://workflowgym.vercel.app/api/demo

## Description

Hello! I built WorkflowGym, a deployable full-stack benchmark for testing tool-using AI agents on simulated FinanceOps billing investigations. The current MVP seeds 20 invoice-dispute scenarios grounded in real public API-pricing patterns, then uses synthetic customer, usage, invoice, and hidden-error fixtures so that each case has deterministic ground truth. A rule-based agent investigates each scenario by calling five finance tools: customer lookup, invoice lookup, usage-event retrieval, contract-term lookup, and invoice-vs-usage comparison.

Every tool call is stored as an auditable trace. The agent produces a structured final decision explaining whether the invoice is correct and what caused the issue, and an evaluator scores the run by checking decision accuracy, cause accuracy, required-tool coverage, and total traced tool calls.

The live FastAPI app exposes API endpoints and a polished dashboard showing benchmark metrics, scenario results, invoice calculations, provenance labels, and trace details.


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

This is intentional. Public pricing pages are useful for modeling how billing systems work, but real customer invoices, contracts, and usage logs are usually private. WorkflowGym therefore uses public sources for domain grounding and synthetic fixtures for controlled benchmark evaluation.

### Source 1: AWS API Gateway Pricing

Link: https://aws.amazon.com/api-gateway/pricing/

This is the primary real-world reference used by the current benchmark.

What this source establishes:

- API products can be priced by received API calls.
- Data transfer can also be part of the bill.
- Pricing can be modeled as usage quantity multiplied by a unit rate.
- AWS REST API pricing examples include `$3.50 per million API calls`.
- AWS API Gateway pricing examples include `$0.09 per GB` for data transfer.

How WorkflowGym uses it:

- The benchmark models a usage-based API billing workflow.
- Each scenario gives the agent invoice quantities, usage records, contract terms, and overage rates.
- The agent must recompute the expected billable usage and compare it with the invoice.
- The UI links every scenario back to this pricing source so it is clear that the benchmark is grounded in a real public billing pattern.

What WorkflowGym does **not** claim:

- It does not claim that Acme AI, Beta Robotics, or any seeded customer is a real AWS customer.
- It does not claim that the seeded invoices are real AWS invoices.
- It does not copy AWS invoices, AWS customer data, or confidential usage logs.
- It does not exactly reproduce AWS's full pricing system, tiers, regions, private API behavior, caching charges, or data-transfer edge cases.
- It uses simplified per-call overage rates so the benchmark remains easy to understand and deterministic.

### Source 2: AWS Price List Bulk API Documentation

Link: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-the-aws-price-list-bulk-api.html

This source is not used directly by the current seed data, but it documents a realistic future path for replacing manually curated pricing facts with programmatic public pricing ingestion.

What this source establishes:

- AWS exposes pricing data through official pricing APIs.
- The Bulk API is intended for consuming large amounts of AWS product and pricing information.
- The documented workflow includes discovering services, listing price lists, and downloading price list files.
- This is the kind of source a production-grade benchmark could use to keep pricing fixtures synchronized with public cloud pricing.

How WorkflowGym could use it later:

- Add a pricing-ingestion job that fetches public cloud pricing data.
- Store real public service codes, regions, SKUs, and unit prices in PostgreSQL.
- Generate benchmark scenarios from real public pricing tables instead of hand-written pricing fixtures.
- Test whether agents can reason over more complex public pricing catalogs.

What WorkflowGym does **not** currently do with it:

- It does not call the AWS Price List Bulk API during the live demo.
- It does not auto-refresh prices.
- It does not store downloaded AWS price files.
- It does not use real AWS SKUs in the current 20 scenarios.

### Source 3: SEC EDGAR APIs

Link: https://www.sec.gov/search-filings/edgar-application-programming-interfaces

This source is listed as a future expansion path, not as a current input to the 20 invoice scenarios.

What this source establishes:

- The SEC provides public API access to EDGAR filing data.
- Public company filings can be used as real-world financial source material.
- A future WorkflowGym benchmark could use public filings for finance, accounting, procurement, or vendor-risk workflows.

How WorkflowGym could use it later:

- Build scenarios where an agent checks public-company facts from filings.
- Add FinanceOps tasks involving revenue, expenses, vendor concentration, risk factors, or public-company metadata.
- Create workflows that combine invoice tools with public financial filings.

What WorkflowGym does **not** currently do with it:

- It does not ingest SEC filings.
- It does not use public-company financial statements in the current benchmark.
- It does not claim that any current scenario is based on a real company filing.

### Synthetic Benchmark Fixtures

The following parts of the current benchmark are synthetic:

- customer names
- usage volumes
- invoice line items
- included allowances
- overage rates
- injected billing errors
- hidden ground truth labels
- final expected outcomes

Why synthetic fixtures are used:

- Real invoices and customer usage logs are usually private.
- A benchmark needs known hidden ground truth so it can score runs deterministically.
- Synthetic fixtures make it possible to test duplicate usage, rate mismatch, allowance errors, and clean control cases safely.
- The same scenarios can be rerun repeatedly with stable expected answers.
- The result is a resume-friendly project that demonstrates agent evaluation mechanics without exposing or fabricating claims about private real-world customer data.

### Current Source Label In The App

In the live UI and `/api/demo` response, each scenario is labeled as:

```text
real_public_reference_plus_synthetic_invoice
```

That means the scenario is grounded in a real public pricing reference, but the customer, invoice, usage data, and hidden error are synthetic benchmark data.

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

