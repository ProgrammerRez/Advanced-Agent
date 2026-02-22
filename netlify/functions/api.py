"""
Netlify Serverless Function Entry Point
======================================
This module wraps the FastAPI application with Mangum so it can run
as an AWS Lambda-compatible Netlify Function. All HTTP requests
sent to /.netlify/functions/api are proxied into the FastAPI app.

Netlify Function path:  /.netlify/functions/api
(Rewritten via netlify.toml redirects to  /api/*)
"""

import sys
import os

# ---------------------------------------------------------------------------
# Path fix: make the project root importable from this subdirectory
# ---------------------------------------------------------------------------
# __file__ is  <repo_root>/netlify/functions/api.py
# We need <repo_root> on sys.path so that `from app import app` works.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# ---------------------------------------------------------------------------
# Import the FastAPI application
# ---------------------------------------------------------------------------
from app import app  # noqa: E402  (import after sys.path manipulation)

# ---------------------------------------------------------------------------
# Wrap with Mangum (ASGI → AWS Lambda handler)
# ---------------------------------------------------------------------------
from mangum import Mangum  # noqa: E402

handler = Mangum(app, lifespan="off")
