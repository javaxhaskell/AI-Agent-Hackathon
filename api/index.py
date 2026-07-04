"""Vercel serverless entrypoint — serves the standalone judge console (ASGI).

Vercel's @vercel/python runtime detects the module-level `app` (a FastAPI ASGI
app) and serves it. This exposes the SELF-CONTAINED console (console/app.py):
the permission-aware-memory demo — page + /api/state, /api/triage, /api/approve,
/api/promote, /api/revoke, /api/permission-flip, /api/demo/reset, /api/trace — all
over a seeded in-memory db. It does NOT run the sim-driven T1 loop (`/api/drive/*`
needs the separate MediaCo sim process); that stays a local `make sim` demo.

Serverless notes: PRECEDENT_MEMORY_DB=:memory: so nothing touches the read-only
filesystem; the demo state seeds once per warm instance (ephemeral across cold
starts — fine for a demo, not a source of truth).
"""
import os
import sys

# Make the repo packages (console, precedent, precedent_memory) importable.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# In-memory demo state — never write to Vercel's read-only disk.
os.environ.setdefault("PRECEDENT_MEMORY_DB", ":memory:")

from console.app import app  # noqa: E402  (ASGI app served by Vercel)

__all__ = ["app"]
