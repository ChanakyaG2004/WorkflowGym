# WorkflowGym Phase 1: Backend Setup

Phase 1 creates the smallest useful backend foundation for WorkflowGym.

In Phase 0, we described the architecture. In Phase 1, we set up the first real pieces of that architecture:

- FastAPI application
- SQLAlchemy database connection setup
- PostgreSQL database URL
- Request-scoped database sessions
- `/health` endpoint

We are not building models, seed data, tools, agents, or evaluators yet. This phase is only about proving the backend can start and knows how it will connect to PostgreSQL.

## What We Are Building

We are building this minimal backend structure:

```text
backend/
  app/
    __init__.py
    main.py

    db/
      __init__.py
      database.py

  requirements.txt
```

The important files are:

```text
backend/app/main.py
backend/app/db/database.py
```

## Why This Phase Exists

Every later part of WorkflowGym depends on database access.

The seed script will need a database session.

The finance tools will need a database session.

The rule-based agent will store tool traces.

The evaluator will store evaluation results.

The API endpoints will load scenarios and runs.

Instead of each part creating its own database connection, we define the database setup once in `backend/app/db/database.py`.

That gives the project one clear source of truth for database access.

## FastAPI App

The FastAPI app lives in:

```text
backend/app/main.py
```

Its job is to create the API application and define routes.

For Phase 1, the only route is:

```text
GET /health
```

The app is created with:

```python
app = FastAPI(title="WorkflowGym API")
```

This creates the backend application object that Uvicorn will run.

## Database Setup

The database setup lives in:

```text
backend/app/db/database.py
```

This file defines:

- `DATABASE_URL`
- `engine`
- `SessionLocal`
- `Base`
- `get_db`

Each one has a specific job.

## `DATABASE_URL`

`DATABASE_URL` tells SQLAlchemy where PostgreSQL is running.

For local development, we use this default:

```text
postgresql+psycopg://workflowgym:workflowgym@localhost:5432/workflowgym
```

This means:

- Database driver: `psycopg`
- Username: `workflowgym`
- Password: `workflowgym`
- Host: `localhost`
- Port: `5432`
- Database name: `workflowgym`

In code, we read it from the environment first:

```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://workflowgym:workflowgym@localhost:5432/workflowgym",
)
```

Why use an environment variable?

Because the database location may change later:

- Local machine
- Docker container
- Test database
- Deployed database

The app code should not need to change for each environment.

## `engine`

The SQLAlchemy engine manages connections to the database.

```python
engine = create_engine(DATABASE_URL)
```

You can think of the engine as the database connection manager.

It does not represent one specific query. It owns the connection pool that SQLAlchemy uses when the app needs to talk to PostgreSQL.

## `SessionLocal`

`SessionLocal` creates database sessions.

```python
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
```

A session is the object we use to:

- Query rows
- Add new rows
- Commit changes
- Roll back failed work

In a web API, each request should usually get its own short-lived database session.

That is why we create a session factory instead of creating one global session.

## `Base`

`Base` is the parent class for future SQLAlchemy models.

```python
class Base(DeclarativeBase):
    """Base class that future SQLAlchemy ORM models will inherit from."""
```

In Phase 2, models will look like this:

```python
class Customer(Base):
    ...
```

That inheritance tells SQLAlchemy:

```text
This Python class maps to a database table.
```

## `get_db`

`get_db` is a FastAPI dependency.

```python
def get_db() -> Generator[Session, None, None]:
    """Provide one database session for a FastAPI request, then close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Its job is:

1. Open a database session.
2. Give it to the request handler.
3. Close it after the request finishes.

The `yield` is important. In FastAPI dependencies, code before `yield` runs before the request handler, and code after `yield` runs after the request handler.

## Health Endpoint

The health endpoint lives in:

```text
backend/app/main.py
```

It checks two things:

1. Is the FastAPI app running?
2. Can the app reach PostgreSQL?

The endpoint uses:

```python
db.execute(text("SELECT 1"))
```

`SELECT 1` is a tiny SQL query. It does not read application data. It only proves that the database connection works.

If the database is reachable, the endpoint returns:

```json
{
  "status": "ok",
  "database": "connected"
}
```

If the database is not reachable, the endpoint returns:

```json
{
  "status": "ok",
  "database": "disconnected"
}
```

Why not crash?

During early development, this makes it easier to distinguish between:

- The API app is broken
- PostgreSQL is simply not running yet

The API can still start even if the database is not currently available.

## Files Created In Phase 1

### `backend/app/db/__init__.py`

Marks `db` as a Python package.

```python
"""Database package for WorkflowGym."""
```

### `backend/app/db/database.py`

Contains the SQLAlchemy setup.

This file is the foundation for all later database work.

## Files Modified In Phase 1

### `backend/app/main.py`

Creates the FastAPI app and defines `/health`.

It imports:

```python
from app.db.database import get_db
```

so route handlers can receive a database session.

## Dependency File

The backend dependencies are listed in:

```text
backend/requirements.txt
```

Current dependencies:

```text
fastapi==0.116.1
uvicorn[standard]==0.35.0
SQLAlchemy==2.0.41
psycopg[binary]==3.2.9
```

What each dependency does:

- `fastapi`: web framework
- `uvicorn`: server that runs the FastAPI app
- `SQLAlchemy`: ORM and database toolkit
- `psycopg`: PostgreSQL database driver

## How To Run The App

From the `backend` directory:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/health
```

If PostgreSQL is not running yet, you should expect:

```json
{
  "status": "ok",
  "database": "disconnected"
}
```

That still means the FastAPI app is working.

## What We Verified

We verified that the backend code compiles:

```bash
backend/.venv/bin/python -m compileall backend/app
```

We also verified that the app imports:

```bash
.venv/bin/python -c 'from app.main import app; print(app.title)'
```

Expected output:

```text
WorkflowGym API
```

## What We Are Not Doing Yet

In Phase 1, we are not yet:

- Creating database tables
- Defining SQLAlchemy models
- Running `create_all`
- Seeding Acme AI data
- Building finance tools
- Running an agent
- Creating evaluation results
- Adding React
- Adding Docker
- Adding an LLM

Those come later.

## Exact Learning Objective

By the end of Phase 1, you should understand:

- How a FastAPI app is created.
- What a route handler is.
- Why `/health` is useful.
- What `DATABASE_URL` represents.
- What the SQLAlchemy engine does.
- What a SQLAlchemy session is.
- Why each request should get its own database session.
- Why future models will inherit from `Base`.
- Why database setup belongs in one shared module.

## What You Should Understand Before Moving On

Before Phase 2, make sure these ideas are clear:

- `FastAPI()` creates the backend application.
- `/health` verifies the app is alive.
- `DATABASE_URL` tells SQLAlchemy where PostgreSQL lives.
- `engine` manages database connections.
- `SessionLocal` creates database sessions.
- `get_db()` provides one session per request and closes it afterward.
- `Base` will be used by the SQLAlchemy models in Phase 2.
- Seeing `"database": "disconnected"` means PostgreSQL is not reachable yet, not necessarily that the FastAPI app is broken.

Once this setup makes sense, the next step is Phase 2: create the SQLAlchemy models for the FinanceOps data, agent traces, and evaluation results.

## Implementation Status

Phase 1 is implemented.

The current backend starts from:

```text
backend/app/main.py
```

The database setup lives in:

```text
backend/app/db/database.py
```

The app still defaults to PostgreSQL:

```text
postgresql+psycopg://workflowgym:workflowgym@localhost:5432/workflowgym
```

For local verification without PostgreSQL, the code can also run against a temporary SQLite database by setting `DATABASE_URL` before import. That is only for lightweight testing; PostgreSQL remains the intended project database.
