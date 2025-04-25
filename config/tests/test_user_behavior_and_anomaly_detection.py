import pytest
import time
from fastapi import FastAPI, Response
from fastapi.testclient import TestClient
from prometheus_client import Counter, Gauge, CollectorRegistry, generate_latest

# --- Setup FastAPI app and Prometheus metrics ---
app = FastAPI()
registry = CollectorRegistry()
USER_BEHAVIOR_COUNTER = Counter('user_behavior_total', 'User behavior events', ['user_id', 'event'], registry=registry)
USER_SESSIONS_COUNTER = Counter('user_sessions_total', 'User session logins', ['user_id'], registry=registry)
ACTIVE_USERS = Gauge('active_users', 'Active users gauge', ['user_id'], registry=registry)
API_REQUESTS_COUNTER = Counter('api_requests_total', 'API request counter', ['endpoint'], registry=registry)
API_REQUEST_LATENCY = Counter('api_request_latency_seconds', 'API latency histogram', ['endpoint'], registry=registry)
REQUEST_RATE_ANOMALY = Gauge('request_rate_anomaly', 'Request rate anomaly metric', ['user_id'], registry=registry)
ERROR_RATE_ANOMALY = Gauge('error_rate_anomaly', 'Error rate anomaly metric', ['user_id'], registry=registry)
LATENCY_ANOMALY = Gauge('latency_anomaly', 'Latency anomaly metric', ['user_id'], registry=registry)
CREDIT_USAGE = Counter('credit_usage_total', 'Total credits used', ['user_id'], registry=registry)
CREDIT_TRANSACTION_COUNT = Counter('credit_transaction_count', 'Number of credit transactions', ['user_id'], registry=registry)
CREDIT_BALANCE = Gauge('credit_balance', 'Current credit balance', ['user_id'], registry=registry)

@app.post('/api/track_behavior')
def track_behavior(user_id: str, event: str):
    USER_BEHAVIOR_COUNTER.labels(user_id=user_id, event=event).inc()
    API_REQUESTS_COUNTER.labels(endpoint='/api/track_behavior').inc()
    API_REQUEST_LATENCY.labels(endpoint='/api/track_behavior').inc(0.05)
    return {"status": "tracked"}

@app.post('/api/login')
def login(user_id: str):
    USER_SESSIONS_COUNTER.labels(user_id=user_id).inc()
    ACTIVE_USERS.labels(user_id=user_id).set(1)
    API_REQUESTS_COUNTER.labels(endpoint='/api/login').inc()
    API_REQUEST_LATENCY.labels(endpoint='/api/login').inc(0.07)
    return {"status": "logged_in"}

@app.post('/api/logout')
def logout(user_id: str):
    ACTIVE_USERS.labels(user_id=user_id).set(0)
    API_REQUESTS_COUNTER.labels(endpoint='/api/logout').inc()
    API_REQUEST_LATENCY.labels(endpoint='/api/logout').inc(0.03)
    return {"status": "logged_out"}

@app.post('/api/health-check')
def health_check():
    API_REQUESTS_COUNTER.labels(endpoint='/api/health-check').inc()
    API_REQUEST_LATENCY.labels(endpoint='/api/health-check').inc(0.01)
    return {"status": "healthy"}

@app.post('/api/non-existent')
def non_existent():
    API_REQUESTS_COUNTER.labels(endpoint='/api/non-existent').inc()
    API_REQUEST_LATENCY.labels(endpoint='/api/non-existent').inc(0.02)
    return Response(status_code=404)

@app.post('/api/detect_anomaly')
def detect_anomaly(user_id: str, anomaly_type: str):
    if anomaly_type == 'request_rate':
        REQUEST_RATE_ANOMALY.labels(user_id=user_id).set(1)
    elif anomaly_type == 'error_rate':
        ERROR_RATE_ANOMALY.labels(user_id=user_id).set(1)
    elif anomaly_type == 'latency':
        LATENCY_ANOMALY.labels(user_id=user_id).set(1)
    return {"status": "anomaly_set"}

@app.post('/api/run-script')
def run_script(user_id: str):
    CREDIT_USAGE.labels(user_id=user_id).inc(10)
    CREDIT_TRANSACTION_COUNT.labels(user_id=user_id).inc()
    CREDIT_BALANCE.labels(user_id=user_id).set(90)
    return {"status": "script_ran"}

@app.post('/api/generate-content')
def generate_content(user_id: str):
    CREDIT_USAGE.labels(user_id=user_id).inc(15)
    CREDIT_TRANSACTION_COUNT.labels(user_id=user_id).inc()
    CREDIT_BALANCE.labels(user_id=user_id).set(75)
    return {"status": "content_generated"}

@app.post('/api/analyze-data')
def analyze_data(user_id: str):
    CREDIT_USAGE.labels(user_id=user_id).inc(20)
    CREDIT_TRANSACTION_COUNT.labels(user_id=user_id).inc()
    CREDIT_BALANCE.labels(user_id=user_id).set(55)
    return {"status": "data_analyzed"}

@app.get('/metrics')
def metrics():
    return Response(generate_latest(registry), media_type='text/plain')

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

# --- TESTS ---
def test_user_behavior_tracking(client):
    user_id = "testuser_e2e"
    # Simulate login
    resp = client.post('/api/login', params={"user_id": user_id})
    assert resp.status_code == 200
    # Track user behavior
    for event in ["login", "profile_view", "metrics_check"]:
        resp = client.post('/api/track_behavior', params={"user_id": user_id, "event": event})
        assert resp.status_code == 200
        time.sleep(0.1)
    # Simulate API requests
    for endpoint in ['/api/health-check', '/api/non-existent']:
        for _ in range(3):
            resp = client.post(endpoint)
            # /api/non-existent returns 404
            assert resp.status_code in (200, 404)
            time.sleep(0.1)
    # Check metrics
    resp = client.get('/metrics')
    content = resp.content.decode('utf-8')
    metrics_to_check = [
        "api_requests_total",
        "api_request_latency_seconds",
        "user_sessions_total",
        "active_users",
    ]
    for metric in metrics_to_check:
        assert metric in content, f"Missing metric: {metric}"
    # Simulate logout
    resp = client.post('/api/logout', params={"user_id": user_id})
    assert resp.status_code == 200

def test_anomaly_detection(client):
    user_id = "testuser_e2e"
    # Simulate login
    resp = client.post('/api/login', params={"user_id": user_id})
    assert resp.status_code == 200
    # Simulate normal traffic
    for _ in range(5):
        resp = client.post('/api/health-check')
        assert resp.status_code == 200
        time.sleep(0.05)
    # Simulate anomaly
    for anomaly_type in ["request_rate", "error_rate", "latency"]:
        resp = client.post('/api/detect_anomaly', params={"user_id": user_id, "anomaly_type": anomaly_type})
        assert resp.status_code == 200
    # Check metrics
    resp = client.get('/metrics')
    content = resp.content.decode('utf-8')
    anomaly_metrics = [
        "request_rate_anomaly",
        "error_rate_anomaly",
        "latency_anomaly",
    ]
    for metric in anomaly_metrics:
        assert metric in content, f"Missing metric: {metric}"
    # Simulate logout
    resp = client.post('/api/logout', params={"user_id": user_id})
    assert resp.status_code == 200

def test_credit_usage_monitoring(client):
    user_id = "testuser_e2e"
    # Simulate login
    resp = client.post('/api/login', params={"user_id": user_id})
    assert resp.status_code == 200
    # Simulate credit-consuming API calls
    credit_endpoints = [
        '/api/run-script',
        '/api/generate-content',
        '/api/analyze-data',
    ]
    for endpoint in credit_endpoints:
        resp = client.post(endpoint, params={"user_id": user_id})
        assert resp.status_code == 200
        time.sleep(0.1)
    # Check metrics
    resp = client.get('/metrics')
    content = resp.content.decode('utf-8')
    credit_metrics = [
        "credit_usage_total",
        "credit_transaction_count",
        "credit_balance",
    ]
    for metric in credit_metrics:
        assert metric in content, f"Missing metric: {metric}"
    # Simulate logout
    resp = client.post('/api/logout', params={"user_id": user_id})
    assert resp.status_code == 200

def test_metrics_endpoint(client):
    resp = client.get('/metrics')
    assert resp.status_code == 200
    content = resp.content.decode('utf-8')
    # Print sample metrics output
    print("\n--- Metrics Output (first 10 lines) ---")
    for line in content.splitlines()[:10]:
        print(line)
    print("--- End Metrics Output ---\n")
