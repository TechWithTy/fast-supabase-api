# Debugging FastAPI 404 for Registered Endpoints in Tests

## Context

**Problem:**
A test for `/api/v1/auth/login` fails with a 404, even though other endpoints under `/api/v1/auth/*` work and pass their tests. The FastAPI app uses routers for most endpoints, but `/login` was originally registered directly on the `app` object or with a different router/prefix setup.

**Symptoms:**
- `POST /api/v1/auth/login` returns 404 in tests.
- Other endpoints like `/api/v1/auth/signin` or `/api/v1/auth/refresh` work fine in both app and tests.
- Test code looks like:
  ```python
  async with AsyncClient(app=app, base_url="http://test") as ac:
      for _ in range(6):
          resp = await ac.post("/api/v1/auth/login", json={"email": email, "password": "wrong"})
      assert resp.status_code == 423
  ```

## Root Cause

- **Router-based endpoints** (using `APIRouter` and `include_router`) are always included with the correct prefix and are available in tests.
- **Directly registered endpoints** (using `@app.post(...)`) may not be present if the test imports a different `app` instance or if the router inclusion logic changes.
- If the endpoint is registered on a router but the router is not included with the correct prefix, the endpoint path will not match the test expectation.

## Solution

- **Best Practice:** Always register endpoints on an `APIRouter`, and include routers with the correct prefix in your main app.
- **For compatibility:** If you want both `/api/v1/auth/login` and `/api/v1/auth/signin` to work, register both on the router:
  ```python
  @router.post("/signin")
  @router.post("/login")
  async def sign_in_with_email(...): ...
  ```
- No need to change the main router setup if other tests are passing; just ensure all expected endpoint paths are registered on the router.

## Checklist for Future Debugging

- [ ] Print all registered routes in the test to confirm endpoint availability.
- [ ] Ensure test POSTs to the exact registered path.
- [ ] Use only one `app = FastAPI()` instance and consistent router patterns.
- [ ] Avoid direct `@app.post` unless absolutely necessary.

---

**Summary:**
If a FastAPI endpoint returns 404 in tests but others work, check if the endpoint is registered on a router and included with the correct prefix. Registering multiple paths on the same handler is a safe, DRY way to support both legacy and new test paths without breaking existing logic.
