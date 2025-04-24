# Debugging FastAPI Redis Lifespan Initialization Issues

## Context

- **Problem**: `RuntimeError: Redis client not initialized via lifespan event.` in tests and/or app.
- **Symptoms**: Even with correct `with TestClient(app) as client:` usage and FastAPI's `lifespan` context, the error persists.
- **Attempts**: 
    - Switched from `@app.on_event` to FastAPI's `lifespan` context for Redis setup/teardown.
    - Ensured no global `TestClient(app)` or global `app` in test files.
    - Changed pytest `client` fixture to `scope="function"`.
    - Confirmed TestClient is only created within a function or fixture.
- **Still Failing**: Redis client is not set on `app.state` during test requests.

## Key Learnings

- **FastAPI's lifespan context** is the only reliable way to set up/tear down resources for both production and tests.
- **TestClient must be created inside a function or function-scoped fixture** to trigger lifespan events.
- **Module-scoped or global TestClient/app usage can break lifespan events** and cause missing dependencies.
- **If lifespan print/log messages do not appear during tests, the context is NOT being triggered.**

## Checklist for Debugging

1. **No global TestClient or app in any test file or conftest.py**
2. **All TestClient instances created inside test functions or function-scoped fixtures**
3. **FastAPI app is created with `lifespan` argument**
4. **TestClient is used as a context manager (`with ... as ...`)**
5. **Redis server is running and accessible at `REDIS_URL`**
6. **Print/log statements in lifespan context to verify execution**

## Current Blockers

- Lifespan context is still not triggered during tests, even after all best practices applied.
- Possible hidden global TestClient/app, or a test/fixture running before the main test and breaking the event chain.
- FastAPI/TestClient/Starlette version mismatch or bug.

## Next Steps

- Add explicit print/logging in lifespan context and in `get_redis_client` to confirm execution order.
- Search entire codebase for any global `TestClient` or `app` creation.
- Consider minimal reproducible example to isolate issue.
- Check FastAPI, Starlette, and httpx versions for compatibility.
- If all else fails, try upgrading/downgrading FastAPI and Starlette.

---

**This file is updated automatically with context from the latest debugging attempts.**
