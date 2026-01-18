"""Test configuration to ensure project package imports work under pytest.

This inserts the Backend-Flask package root into sys.path so tests
can import top-level packages like `service` when pytest is run from
the tests folder or from other working directories.
"""

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parent.parent
ROOT_STR = str(ROOT)
if ROOT_STR not in sys.path:
    sys.path.insert(0, ROOT_STR)
