import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:////tmp/workflowgym_vercel.db")
os.environ.setdefault("AUTO_SEED_DEMO", "true")

from app.main import app  # noqa: E402
