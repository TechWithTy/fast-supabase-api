import os
import sys
import time
from fastapi.testclient import TestClient

# Add the project root to Python path first
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now add the backend directory to the path
backend_dir = os.path.join(project_root, 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import FastAPI app
try:
    from app.main import app
except ImportError:
    raise ImportError("FastAPI app instance could not be imported. Update the import path in test_prometheus.py.")

client = TestClient(app)

def test_prometheus_metrics():
    """
    Test function to generate some metrics for Prometheus by making API requests.
    """
    print("Making test requests to generate metrics...")
    # Make several requests to different endpoints to generate metrics
    for _ in range(3):
        # Try accessing the docs page
        response = client.get('/docs')
        print(f"Docs request status: {response.status_code}")
        # Try accessing a non-existent page to generate 404 metrics
        response = client.get('/non-existent-page')
        print(f"404 request status: {response.status_code}")
        # Try accessing the metrics endpoint
        response = client.get('/metrics')
        print(f"Metrics request status: {response.status_code}")
        time.sleep(0.1)

    # Now verify metrics were collected by checking the /metrics endpoint
    metrics_response = client.get('/metrics')
    metrics_content = metrics_response.content.decode('utf-8')

    print("\n===== PROMETHEUS METRICS VERIFICATION =====")
    print(f"Metrics endpoint status: {metrics_response.status_code}")
    # Print a sample of the metrics
    print("\n--- Metrics Output (first 20 lines) ---")
    for line in metrics_content.splitlines()[:20]:
        print(line)
    print("--- End Metrics Output ---\n")

    # Check for some expected metric names
    assert 'api_requests_total' in metrics_content or 'http_requests_total' in metrics_content, "Expected request counter metric not found."
    assert 'api_request_latency_seconds' in metrics_content or 'http_request_duration_seconds' in metrics_content, "Expected latency metric not found."
    print("Prometheus metrics successfully collected and verified.")

if __name__ == '__main__':
    test_prometheus_metrics()
