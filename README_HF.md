---
title: WorkflowGym
emoji: 🧾
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# WorkflowGym

Backend simulator for evaluating tool-using AI agents on FinanceOps billing investigations.

Open API docs at `/docs`.

Demo endpoints:

- `GET /health`
- `GET /scenarios`
- `POST /scenarios/duplicate_usage_001/run`
- `GET /runs`
- `GET /metrics/summary`

The public demo runs with SQLite and auto-seeded data. The production deployment path uses Docker + PostgreSQL.
