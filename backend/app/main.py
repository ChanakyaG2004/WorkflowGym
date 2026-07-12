import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import func, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.agents.rule_based_agent import run_rule_based_agent
from app.db.database import SessionLocal, get_db
from app.db.init_db import init_db
from app.db.models import AgentRun, EvaluationResult, Scenario
from app.evaluation.evaluator import evaluate_run
from app.schemas.metrics import MetricsSummary
from app.schemas.run import AgentRunRead
from app.schemas.scenario import ScenarioRead
from app.seed.seed_acme import seed_acme, seed_acme_if_missing
from app.ui import render_home_page


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Create database tables at startup when PostgreSQL is reachable."""
    try:
        init_db()
        if os.getenv("AUTO_SEED_DEMO", "false").lower() == "true":
            seed_acme_if_missing()
    except SQLAlchemyError:
        # The app can still start; /health will report database status.
        pass
    yield


app = FastAPI(
    title="WorkflowGym API",
    description=(
        "Backend simulator for evaluating tool-using AI agents on "
        "FinanceOps billing investigations."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
def home() -> HTMLResponse:
    """Serve the human-friendly project demo page."""
    return render_home_page()


@app.get("/health")
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    """Confirm that the API is running and report whether PostgreSQL is reachable."""
    try:
        # SELECT 1 is a tiny query that proves the database connection works.
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return {"status": "ok", "database": "disconnected"}

    return {"status": "ok", "database": "connected"}


@app.get("/scenarios", response_model=list[ScenarioRead])
def list_scenarios(db: Session = Depends(get_db)) -> list[Scenario]:
    """List available scenarios without exposing hidden causes."""
    return list(db.scalars(select(Scenario).order_by(Scenario.id)).all())


@app.post("/scenarios/{scenario_id}/run", response_model=AgentRunRead)
def run_scenario(scenario_id: str, db: Session = Depends(get_db)) -> AgentRun:
    """Run the rule-based agent and evaluate the result."""
    scenario = db.scalar(select(Scenario).where(Scenario.scenario_key == scenario_id))
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")

    run = run_rule_based_agent(db, scenario)
    evaluate_run(db, run, scenario)

    full_run = db.scalar(
        select(AgentRun)
        .where(AgentRun.id == run.id)
        .options(
            selectinload(AgentRun.steps),
            selectinload(AgentRun.evaluation_result),
        )
    )
    if full_run is None:
        raise HTTPException(status_code=500, detail="Run was not created")
    return full_run


@app.get("/runs", response_model=list[AgentRunRead])
def list_runs(db: Session = Depends(get_db)) -> list[AgentRun]:
    """List agent runs with their traces and evaluation results."""
    return list(
        db.scalars(
            select(AgentRun)
            .options(
                selectinload(AgentRun.steps),
                selectinload(AgentRun.evaluation_result),
            )
            .order_by(AgentRun.id)
        ).all()
    )


@app.get("/runs/{run_id}", response_model=AgentRunRead)
def get_run(run_id: int, db: Session = Depends(get_db)) -> AgentRun:
    """Fetch one run, including tool-call trace and evaluation."""
    run = db.scalar(
        select(AgentRun)
        .where(AgentRun.id == run_id)
        .options(
            selectinload(AgentRun.steps),
            selectinload(AgentRun.evaluation_result),
        )
    )
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@app.get("/metrics/summary", response_model=MetricsSummary)
def get_metrics_summary(db: Session = Depends(get_db)) -> MetricsSummary:
    """Return aggregate metrics across evaluated agent runs."""
    total_scenarios = db.scalar(select(func.count(Scenario.id))) or 0
    total_runs = db.scalar(select(func.count(AgentRun.id))) or 0
    passed_runs = (
        db.scalar(select(func.count(EvaluationResult.id)).where(EvaluationResult.passed))
        or 0
    )
    aggregates = db.execute(
        select(
            func.avg(EvaluationResult.score),
            func.avg(EvaluationResult.tool_accuracy),
            func.avg(EvaluationResult.run_duration_ms),
            func.sum(EvaluationResult.total_tool_call_count),
            func.sum(EvaluationResult.detected_overcharge_cents),
            func.sum(EvaluationResult.duplicate_usage_quantity),
        )
    ).one()

    pass_rate = (passed_runs / total_runs * 100) if total_runs else 0

    return MetricsSummary(
        total_scenarios=total_scenarios,
        total_runs=total_runs,
        passed_runs=passed_runs,
        pass_rate=round(pass_rate, 2),
        average_score=round(float(aggregates[0] or 0), 2),
        average_tool_accuracy=round(float(aggregates[1] or 0), 2),
        average_run_duration_ms=round(float(aggregates[2] or 0), 2),
        total_tool_calls=int(aggregates[3] or 0),
        total_detected_overcharge_cents=int(aggregates[4] or 0),
        total_duplicate_usage_quantity=int(aggregates[5] or 0),
    )


@app.get("/demo")
def run_demo() -> dict[str, object]:
    """Run the complete demo in one request for stateless public deployments."""
    seed_acme(reset=True)
    db = SessionLocal()
    try:
        run = run_scenario("duplicate_usage_001", db)
        summary = get_metrics_summary(db)
        return {
            "github": "https://github.com/ChanakyaG2004/WorkflowGym",
            "scenario": "duplicate_usage_001",
            "run_id": run.id,
            "decision": run.final_answer["decision"] if run.final_answer else None,
            "cause": run.final_answer["cause"] if run.final_answer else None,
            "score": run.evaluation_result.score if run.evaluation_result else None,
            "tool_accuracy": (
                run.evaluation_result.tool_accuracy if run.evaluation_result else None
            ),
            "required_tools_called": (
                f"{run.evaluation_result.called_required_tool_count}/"
                f"{run.evaluation_result.required_tool_count}"
                if run.evaluation_result
                else None
            ),
            "tool_calls_traced": len(run.steps),
            "duplicate_usage_detected": (
                run.evaluation_result.duplicate_usage_quantity
                if run.evaluation_result
                else None
            ),
            "overcharge_detected_dollars": (
                run.evaluation_result.detected_overcharge_cents / 100
                if run.evaluation_result
                else None
            ),
            "passed": run.evaluation_result.passed if run.evaluation_result else None,
            "metrics_summary": summary.model_dump(),
        }
    finally:
        db.close()
