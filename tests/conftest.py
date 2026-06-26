"""Shared test fixtures and import setup for the Marketing AI test suite.

``app.py`` lives at the repository root and pulls in Streamlit at import time.
Streamlit emits a benign "missing ScriptRunContext" warning when imported
outside ``streamlit run`` — it is filtered here so the test output stays clean.
The rule-engine and scoring functions under test are plain Python and do not
need a running Streamlit session.
"""
import sys
import warnings
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

warnings.filterwarnings("ignore", message=".*ScriptRunContext.*")


@pytest.fixture(scope="session")
def app_module():
    """Import the Streamlit app module once for the whole test session."""
    import app

    return app
