from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Customer(Base):
    """A company whose billing data the agent can investigate."""

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    pricing_plans: Mapped[list[PricingPlan]] = relationship(back_populates="customer")
    usage_events: Mapped[list[UsageEvent]] = relationship(back_populates="customer")
    invoices: Mapped[list[Invoice]] = relationship(back_populates="customer")


class PricingPlan(Base):
    """Contract terms for a customer's API usage."""

    __tablename__ = "pricing_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    included_api_calls: Mapped[int] = mapped_column(Integer)
    overage_rate_cents: Mapped[int] = mapped_column(Integer)

    customer: Mapped[Customer] = relationship(back_populates="pricing_plans")


class UsageEvent(Base):
    """A usage batch recorded by the billing system."""

    __tablename__ = "usage_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    month: Mapped[str] = mapped_column(String(7), index=True)
    event_type: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int] = mapped_column(Integer)
    is_duplicate: Mapped[bool] = mapped_column(Boolean, default=False)

    customer: Mapped[Customer] = relationship(back_populates="usage_events")


class Invoice(Base):
    """An invoice sent to a customer for one billing month."""

    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    month: Mapped[str] = mapped_column(String(7), index=True)
    total_cents: Mapped[int] = mapped_column(Integer)

    customer: Mapped[Customer] = relationship(back_populates="invoices")
    line_items: Mapped[list[InvoiceLineItem]] = relationship(back_populates="invoice")


class InvoiceLineItem(Base):
    """One charge line on an invoice."""

    __tablename__ = "invoice_line_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"))
    description: Mapped[str] = mapped_column(String(255))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price_cents: Mapped[int] = mapped_column(Integer)
    amount_cents: Mapped[int] = mapped_column(Integer)

    invoice: Mapped[Invoice] = relationship(back_populates="line_items")


class Scenario(Base):
    """A hidden-ground-truth task for an agent to solve."""

    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(255))
    month: Mapped[str] = mapped_column(String(7))
    prompt: Mapped[str] = mapped_column(Text)
    expected_outcome: Mapped[str] = mapped_column(String(100))
    hidden_cause: Mapped[str] = mapped_column(String(100))
    required_tools: Mapped[list[str]] = mapped_column(JSON)

    runs: Mapped[list[AgentRun]] = relationship(back_populates="scenario")


class AgentRun(Base):
    """One attempt to solve a scenario."""

    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id"))
    status: Mapped[str] = mapped_column(String(50), default="running")
    final_answer: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    scenario: Mapped[Scenario] = relationship(back_populates="runs")
    steps: Mapped[list[AgentStep]] = relationship(
        back_populates="agent_run",
        order_by="AgentStep.step_number",
    )
    evaluation_result: Mapped[EvaluationResult | None] = relationship(
        back_populates="agent_run",
        uselist=False,
    )


class AgentStep(Base):
    """One tool call made during an agent run."""

    __tablename__ = "agent_steps"

    id: Mapped[int] = mapped_column(primary_key=True)
    agent_run_id: Mapped[int] = mapped_column(ForeignKey("agent_runs.id"))
    step_number: Mapped[int] = mapped_column(Integer)
    tool_name: Mapped[str] = mapped_column(String(100))
    tool_input: Mapped[dict[str, Any]] = mapped_column(JSON)
    tool_output: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    agent_run: Mapped[AgentRun] = relationship(back_populates="steps")


class EvaluationResult(Base):
    """Evaluator judgment for one agent run."""

    __tablename__ = "evaluation_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    agent_run_id: Mapped[int] = mapped_column(ForeignKey("agent_runs.id"), unique=True)
    decision_correct: Mapped[bool] = mapped_column(Boolean)
    cause_correct: Mapped[bool] = mapped_column(Boolean)
    tool_accuracy: Mapped[int] = mapped_column(Integer)
    score: Mapped[int] = mapped_column(Integer)
    required_tool_count: Mapped[int] = mapped_column(Integer)
    called_required_tool_count: Mapped[int] = mapped_column(Integer)
    missing_required_tool_count: Mapped[int] = mapped_column(Integer)
    total_tool_call_count: Mapped[int] = mapped_column(Integer)
    run_duration_ms: Mapped[int] = mapped_column(Integer)
    detected_overcharge_cents: Mapped[int] = mapped_column(Integer)
    duplicate_usage_quantity: Mapped[int] = mapped_column(Integer)
    passed: Mapped[bool] = mapped_column(Boolean)
    details: Mapped[dict[str, Any]] = mapped_column(JSON)

    agent_run: Mapped[AgentRun] = relationship(back_populates="evaluation_result")
