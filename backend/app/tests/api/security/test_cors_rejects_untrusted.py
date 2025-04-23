import pytest
pytestmark = pytest.mark.anyio("asyncio")
from starlette.testclient import TestClient

from app.main import app


def test_cors_rejects_untrusted_origin():
    client = TestClient(app)
    response = client.options(
        "/api/some-protected-endpoint",
        headers={
            "Origin": "http://evil.com",
            "Access-Control-Request-Method": "POST",
        },
    )
    # Should not allow CORS for untrusted origins
    assert "access-control-allow-origin" not in response.headers
    assert response.status_code in (400, 403, 404)
