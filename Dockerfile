FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860
ENV DATABASE_URL=sqlite+pysqlite:////tmp/workflowgym_demo.db
ENV AUTO_SEED_DEMO=true

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

EXPOSE 7860

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
