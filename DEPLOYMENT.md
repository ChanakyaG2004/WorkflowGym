# Deployment Guide

WorkflowGym is currently a backend-only FastAPI service with PostgreSQL.

The simplest deployable unit is the Dockerized API in:

```text
backend/Dockerfile
```

## Required Environment Variables

```text
DATABASE_URL
PORT
```

Example:

```text
DATABASE_URL=postgresql+psycopg://workflowgym:workflowgym@localhost:5432/workflowgym
PORT=8000
```

## Local Docker Demo

Start the API and PostgreSQL:

```bash
docker compose up --build
```

Seed the demo scenario:

```bash
docker compose exec api python -m app.seed.seed_acme
```

Run the smoke test:

```bash
docker compose exec api python -m app.scripts.smoke_test
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Hosted Deployment Shape

Use one web service and one PostgreSQL database.

The web service should:

- Build from `backend/Dockerfile`
- Expose the configured `PORT`
- Set `DATABASE_URL` to the hosted PostgreSQL connection string
- Run the default Docker command

The included `render.yaml` defines:

- `workflowgym-api`: Docker web service
- `workflowgym-db`: managed PostgreSQL database
- `AUTO_SEED_DEMO=true`: seeds the demo scenario when missing

The app creates tables on startup for the MVP. If `AUTO_SEED_DEMO` is disabled, seed the demo data once:

```bash
python -m app.seed.seed_acme
```

For a production-grade version, replace startup `create_all` with Alembic migrations.

## Demo Flow

After deployment:

1. Open `/` for the human-friendly UI.
2. Click `Run Live Demo`.
3. Open `/docs` for the API surface.
4. Run `POST /scenarios/duplicate_usage_001/run` for the raw API flow.
5. Open `GET /metrics/summary`.
6. Show the tool trace, evaluator result, 100% pass rate, 100 score, 5/5 required tools called, 5 stored tool calls, 50,000 duplicate calls detected, and $2,000 overcharge detected.

That flow demonstrates the core resume value of the project: tool-using agent evaluation with traceability.

## Hugging Face Demo Note

The root [Dockerfile](Dockerfile) is for a lightweight public Hugging Face Spaces demo. It runs the same FastAPI app with SQLite and `AUTO_SEED_DEMO=true`.

Use the Render/PostgreSQL path for the stronger production-style deployment.

## Vercel Demo

The [api/index.py](api/index.py), [requirements.txt](requirements.txt), and [vercel.json](vercel.json) files support a lightweight Vercel demo deployment.

This demo uses SQLite in `/tmp` and auto-seeded data, so it is best for public API exploration rather than persistent production storage.

Because serverless `/tmp` storage is not a durable database, the Vercel demo includes:

```text
GET /demo
```

That endpoint seeds, runs, evaluates, and returns metrics in one request.

Deploy:

```bash
npx vercel --prod
```
