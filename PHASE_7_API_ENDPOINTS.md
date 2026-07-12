# WorkflowGym Phase 7: API Endpoints

Phase 7 exposes the backend milestone through FastAPI.

The implementation lives in:

```text
backend/app/main.py
```

## Implemented Endpoints

### `GET /health`

Checks whether the API is running and whether the database is reachable.

### `GET /scenarios`

Lists available scenarios.

This endpoint does not expose hidden ground truth like `expected_outcome` or `hidden_cause`.

### `POST /scenarios/{scenario_id}/run`

Runs a scenario.

For the MVP:

```text
POST /scenarios/duplicate_usage_001/run
```

This endpoint:

1. Loads the scenario.
2. Creates an `AgentRun`.
3. Runs the rule-based agent.
4. Stores every `AgentStep`.
5. Evaluates the run.
6. Returns the run, trace, final answer, and evaluation result.

### `GET /runs`

Lists all agent runs.

### `GET /runs/{run_id}`

Fetches one run with:

- final answer
- tool-call trace
- evaluation result

### `GET /metrics/summary`

Returns aggregate metrics across evaluated runs:

- total scenarios
- total runs
- passed runs
- pass rate
- average score
- average tool accuracy
- average run duration
- total tool calls
- total detected overcharge
- total duplicate usage quantity

## How To Try It

Start PostgreSQL, seed the data, then run the API:

```bash
cd backend
source .venv/bin/activate
python -m app.seed.seed_acme
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

FastAPI automatically generates interactive API docs.

## What You Should Understand

- API routes are thin wrappers around application logic.
- The route does not contain the finance investigation itself.
- The route calls the agent runner and evaluator.
- Response schemas control what the API returns.
- Hidden ground truth should not be exposed through normal scenario listing.
