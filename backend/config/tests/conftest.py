import os
import sys

import pytest
from fastapi.testclient import TestClient

# Add the project root directory to Python's module search path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Also add the backend directory to the path
backend_dir = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_dir)

# Import the FastAPI app (update this import if your app is elsewhere)
try:
    from app.main import app
except ImportError:
    # If app.main does not exist, update this import path accordingly
    app = None

# Set environment variable to indicate tests that need authentication should be skipped
os.environ['SKIP_AUTH_TESTS'] = 'True'

@pytest.fixture(scope="session")
def test_client():
    """
    Provides a FastAPI TestClient for API testing.
    """
    if app is None:
        raise RuntimeError("FastAPI app instance could not be imported. Update the import path in conftest.py.")
    client = TestClient(app)
    yield client
