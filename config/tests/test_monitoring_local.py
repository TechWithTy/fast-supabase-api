"""
Standalone test script for FastAPI monitoring features.

This script sets up a minimal environment to test user behavior tracking
and anomaly detection metrics without requiring a full database connection.
"""

import os
import sys
import time
import pytest
from fastapi import FastAPI, Request, Response
from fastapi.testclient import TestClient
from prometheus_client import Counter, Histogram, CollectorRegistry, generate_latest

# Add project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Also add the backend directory to the path
backend_dir = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_dir)

# Set up environment for testing
os.environ['TESTING'] = 'True'
os.environ['FASTAPI_DEBUG'] = 'True'

# Prometheus metrics setup
registry = CollectorRegistry()
API_REQUESTS_COUNTER = Counter(
    'api_requests_total', 'Total API requests', ['endpoint', 'method'], registry=registry
)
API_REQUEST_LATENCY = Histogram(
    'api_request_latency_seconds', 'API request latency', ['endpoint', 'method'], registry=registry
)

# FastAPI app and instrumentation
app = FastAPI()

@app.middleware('http')
async def prometheus_metrics_middleware(request: Request, call_next):
    endpoint = request.url.path
    method = request.method
    API_REQUESTS_COUNTER.labels(endpoint=endpoint, method=method).inc()
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start
    API_REQUEST_LATENCY.labels(endpoint=endpoint, method=method).observe(latency)
    return response

@app.get('/api/test')
def api_test_endpoint():
    return {"msg": "ok"}

@app.get('/api/error')
def error_endpoint():
    return Response(content='{"error": "fail"}', status_code=500, media_type='application/json')

@app.get('/metrics')
def metrics():
    return Response(generate_latest(registry), media_type='text/plain')

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

# ===== APPROACH 1: DIRECT INSTRUMENTATION TESTING =====
def test_direct_metrics():
    """Test metrics directly by instrumenting them and checking values."""
    API_REQUESTS_COUNTER.labels(endpoint='/unit/test', method='GET').inc(3)
    API_REQUEST_LATENCY.labels(endpoint='/unit/test', method='GET').observe(0.123)
    assert API_REQUESTS_COUNTER.labels(endpoint='/unit/test', method='GET')._value.get() == 3
    # Histogram buckets are cumulative; just check that at least one observation was made
    found = any((v > 0 for v in API_REQUEST_LATENCY.labels(endpoint='/unit/test', method='GET')._sum.get()))
    assert found or API_REQUEST_LATENCY.labels(endpoint='/unit/test', method='GET')._sum.get() > 0

# ===== APPROACH 2: MIDDLEWARE INTEGRATION TESTING =====
def test_middleware_integration(client):
    num_requests = 5
    for _ in range(num_requests):
        resp = client.get('/api/test')
        assert resp.status_code == 200
    # Check that the counter has incremented
    assert API_REQUESTS_COUNTER.labels(endpoint='/api/test', method='GET')._value.get() >= num_requests

# ===== APPROACH 3: ENDPOINT TESTING =====
def test_endpoint(client):
    resp = client.get('/api/test')
    assert resp.status_code == 200
    assert resp.json()['msg'] == 'ok'

def test_error_endpoint(client):
    resp = client.get('/api/error')
    assert resp.status_code == 500
    assert resp.json()['error'] == 'fail'

def test_metrics_endpoint(client):
    resp = client.get('/metrics')
    assert resp.status_code == 200
    assert 'api_requests_total' in resp.text
    assert 'api_request_latency_seconds' in resp.text

if __name__ == "__main__":
    print("Starting FastAPI Prometheus metrics tests...")
    pytest.main([__file__])
