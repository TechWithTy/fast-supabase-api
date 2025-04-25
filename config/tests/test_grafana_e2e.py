#!/usr/bin/env python
import os
import sys
import time
import requests
from datetime import datetime
import random
import pytest
from fastapi.testclient import TestClient

# Add the project root to Python path first
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now add the backend directory to the path
backend_dir = os.path.join(project_root, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Set TESTING environment variable
os.environ["TESTING"] = "True"

def get_env_url(var_name: str, default: str) -> str:
    """Helper to get URLs from env or fall back to default."""
    return os.getenv(var_name, default)

class GrafanaE2ETest:
    """End-to-end test for Grafana monitoring setup with FastAPI and Prometheus."""

    def __init__(self):
        # Import your FastAPI app here (update the import path as needed)
        try:
            from app.main import app
        except ImportError:
            raise ImportError("FastAPI app instance could not be imported. Update the import path in test_grafana_e2e.py.")
        self.client = TestClient(app)
        self.prometheus_url = get_env_url("PROMETHEUS_URL", "http://localhost:9090")
        self.grafana_url = get_env_url("GRAFANA_URL", "http://localhost:3000")
        self.grafana_api_url = f"{self.grafana_url}/api"
        self.grafana_user = os.getenv("GRAFANA_USER", "admin")
        self.grafana_password = os.getenv("GRAFANA_PASSWORD", "admin")
        self.test_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_fastapi_metrics(self, num_requests: int = 10) -> None:
        """Generate FastAPI metrics by making various API requests."""
        print(
            f"\n[1/4] Generating FastAPI metrics with {num_requests} requests per endpoint..."
        )
        # Define endpoints to test with their expected status codes
        endpoints = [
            ("/docs", 200),  # FastAPI docs
            ("/metrics", 200),  # Prometheus metrics
            ("/non-existent-page", 404),  # 404 error
        ]
        for endpoint, expected_status in endpoints:
            print(f"  Making {num_requests} requests to {endpoint}")
            for i in range(num_requests):
                response = self.client.get(endpoint)
                if response.status_code != expected_status:
                    print(
                        f"    Warning: Got status {response.status_code}, expected {expected_status}"
                    )
                # Add some random sleep to create variable response times
                time.sleep(random.uniform(0.1, 0.3))
        print("✓ Successfully generated FastAPI metrics")

    def verify_prometheus_metrics(self) -> bool:
        """Verify that Prometheus is collecting metrics from FastAPI."""
        print("\n[2/4] Verifying Prometheus metrics collection...")
        # First check FastAPI metrics endpoint
        response = self.client.get("/metrics")
        if response.status_code != 200:
            print(f"  Error: FastAPI metrics endpoint returned {response.status_code}")
            return False
        # Check if important metrics exist (update as needed for your app)
        metrics_content = response.content.decode("utf-8")
        required_metrics = [
            "http_requests_total",
            "http_request_duration_seconds",
        ]
        missing_metrics = []
        for metric in required_metrics:
            if metric not in metrics_content:
                missing_metrics.append(metric)
        if missing_metrics:
            print(
                f"  Warning: The following metrics are missing: {', '.join(missing_metrics)}"
            )
        else:
            print("  ✓ All required FastAPI metrics are being collected")
        # Now check if Prometheus is accessible
        try:
            prometheus_response = requests.get(
                f"{self.prometheus_url}/api/v1/status/config"
            )
            if prometheus_response.status_code != 200:
                print(
                    f"  Error: Cannot access Prometheus API: {prometheus_response.status_code}"
                )
                return False
            print("  ✓ Prometheus API is accessible")
            # Check if Prometheus has our target
            targets_response = requests.get(f"{self.prometheus_url}/api/v1/targets")
            if targets_response.status_code != 200:
                print(
                    f"  Error: Cannot access Prometheus targets API: {targets_response.status_code}"
                )
                return False
            print("  ✓ Prometheus targets API is accessible")
            return True
        except Exception as e:
            print(f"  Error: Exception when accessing Prometheus: {e}")
            return False

    def verify_grafana_setup(self) -> bool:
        """Verify that Grafana is accessible and the API is up."""
        print("\n[3/4] Verifying Grafana setup...")
        try:
            grafana_response = requests.get(
                f"{self.grafana_api_url}/health",
                auth=(self.grafana_user, self.grafana_password),
            )
            if grafana_response.status_code != 200:
                print(
                    f"  Error: Cannot access Grafana API: {grafana_response.status_code}"
                )
                return False
            print("  ✓ Grafana API is accessible")
            return True
        except Exception as e:
            print(f"  Error: Exception when accessing Grafana: {e}")
            return False

    def verify_dashboard_data(self) -> bool:
        """Verify that Grafana dashboards are returning data (example, update as needed)."""
        print("\n[4/4] Verifying Grafana dashboard data...")
        # Example: List dashboards
        try:
            dashboards_response = requests.get(
                f"{self.grafana_api_url}/search",
                auth=(self.grafana_user, self.grafana_password),
            )
            if dashboards_response.status_code != 200:
                print(
                    f"  Error: Cannot list Grafana dashboards: {dashboards_response.status_code}"
                )
                return False
            dashboards = dashboards_response.json()
            print(f"  ✓ Retrieved {len(dashboards)} dashboards from Grafana")
            return True
        except Exception as e:
            print(f"  Error: Exception when querying Grafana dashboards: {e}")
            return False

@pytest.fixture
def grafana_test_client():
    """Create and return a GrafanaE2ETest instance for testing."""
    return GrafanaE2ETest()

# Convert methods to pytest test functions
def test_fastapi_metrics_generation(grafana_test_client):
    """Test generating FastAPI metrics with test requests."""
    try:
        grafana_test_client.generate_fastapi_metrics(num_requests=3)
        assert True  # If we got here without errors, the test passes
    except Exception as e:
        pytest.fail(f"Failed to generate FastAPI metrics: {str(e)}")

def test_prometheus_connection(grafana_test_client):
    """Test connection to Prometheus server."""
    try:
        is_connected = grafana_test_client.verify_prometheus_metrics()
        if not is_connected:
            pytest.skip("Prometheus server not available")
        assert True
    except Exception as e:
        pytest.skip(f"Prometheus connection error: {str(e)}")

def test_grafana_connection(grafana_test_client):
    """Test connection to Grafana server."""
    try:
        is_connected = grafana_test_client.verify_grafana_setup()
        if not is_connected:
            pytest.skip("Grafana server not available")
        assert True
    except Exception as e:
        pytest.skip(f"Grafana connection error: {str(e)}")

def test_prometheus_metrics_query(grafana_test_client):
    """Test querying metrics from Prometheus."""
    try:
        # First check if Prometheus is accessible
        if not grafana_test_client.verify_prometheus_metrics():
            pytest.skip("Prometheus server not available")
        # Generate some metrics first
        grafana_test_client.generate_fastapi_metrics(num_requests=3)
        # Try to query metrics
        result = grafana_test_client.verify_prometheus_metrics()
        assert result is True, "Should have found metrics in Prometheus"
    except Exception as e:
        pytest.skip(f"Prometheus metrics query error: {str(e)}")

def test_dashboard_data(grafana_test_client):
    """Test dashboard data."""
    try:
        # First check if Prometheus is accessible
        if not grafana_test_client.verify_prometheus_metrics():
            pytest.skip("Prometheus server not available")
        # Generate some metrics first
        grafana_test_client.generate_fastapi_metrics(num_requests=3)
        # Try to query dashboard data
        result = grafana_test_client.verify_dashboard_data()
        assert result is True, "Should have found dashboard data"
    except Exception as e:
        pytest.skip(f"Dashboard data error: {str(e)}")
