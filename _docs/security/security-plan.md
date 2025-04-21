# API Security Plan for Lead Ignite

This document outlines required and recommended security controls for all API endpoints in the Lead Ignite platform. It is based on a review of the current codebase, API structure, and best practices for SaaS, CRM, and AI-integrated applications.

---

## 1. Authentication

- **Primary:** Use Supabase Auth for user authentication (JWT-based, supports social login).
- **OAuth:** For external integrations (e.g., GHL, VAPI, ElevenLabs), use secure OAuth flows and never expose client secrets in the frontend.
- **Session Security:**
  - Store tokens securely (HTTP-only cookies or secure storage).
  - Rotate and expire tokens regularly.
  - For sensitive actions, require recent authentication (re-auth or short-lived tokens).

## 2. Authorization

- **Role-Based Access Control (RBAC):**
  - Enforce roles (admin, agent, user, etc.) on every endpoint.
  - Check permissions server-side for all sensitive operations (CRUD on leads, calls, users, assistants).
- **Row-Level Security (RLS):**
  - Use Supabase/Postgres RLS for data access, ensuring users can only access their own records.
  - Never trust client-side role claims.

## 3. Input Validation & Sanitization

- **Strict Validation:**
  - Use Zod (frontend) and Pydantic/FastAPI (backend) for schema validation.
  - Reject requests with missing or malformed fields.
  - Enforce strong types and constraints (e.g., email format, phone regex, enum status).
- **Sanitization:**
  - Sanitize all user input to prevent XSS, SQL injection, and command injection.
  - Use parameterized queries and ORM protections for all database access.

## 4. Rate Limiting & Abuse Prevention

- **API Rate Limits:**
  - Apply per-user and per-IP rate limits to all endpoints (especially auth, lead gen, and webhooks).
  - Use middleware (e.g., FastAPI-limiter, Next.js middleware, or Supabase edge functions).
- **Brute Force Protection:**
  - Lock accounts or require CAPTCHA after repeated failed auth attempts.

## 5. Secrets & Sensitive Data

- **Environment Variables:**
  - Store all API keys, tokens, and secrets in environment variables (never commit to git).
  - Use secret managers (Supabase Vault, AWS Secrets Manager, etc.) for production.
- **Token Handling:**
  - Never log or expose tokens in responses or client-side code.
  - Use short-lived tokens for webhooks and external API calls.

## 6. Error Handling & Logging

- **Consistent Error Responses:**
  - Do not leak stack traces or sensitive info in API errors.
  - Use generic error messages for 4xx/5xx responses.
- **Logging:**
  - Log all auth events, permission denials, and suspicious activity (with timestamps and user IDs).
  - Use centralized logging (e.g., ELK, Loki, Supabase logs) and monitor for anomalies.

## 7. CORS & CSRF

- **CORS:**
  - Restrict allowed origins to trusted domains.
  - Do not use `*` in production.
- **CSRF:**
  - Use CSRF tokens for all state-changing requests from browsers.
  - Prefer same-site cookies for session tokens.

## 8. Edge Cases & Advanced Threats

- **Replay Attacks:**
  - Use nonces/timestamps for webhooks and sensitive actions.
  - Reject requests with old or duplicate nonces.
- **Privilege Escalation:**
  - Never allow users to modify their role or access level via API.
  - Double-check all role assignments and permission checks.
- **Injection Attacks:**
  - Validate and sanitize all input, especially in dynamic queries or external API calls.
- **Third-Party Integrations:**
  - Scope OAuth tokens to minimum permissions.
  - Regularly audit and rotate third-party credentials.

## 9. Testing & CI/CD

- **Automated Security Tests:**
  - Include tests for auth, permissions, and input validation in your CI pipeline.
  - Use tools like OWASP ZAP, Snyk, and dependency scanning.
- **End-to-End Tests:**
  - Test real-world flows, ensuring data created/modified is cleaned up after tests.
  - Avoid flaky tests by isolating test data and using proper async handling.

## 10. Monitoring & Incident Response

- **Audit Trails:**
  - Record all user actions that modify data.
  - Provide admins with access to audit logs for investigation.
- **Alerts:**
  - Set up alerts for suspicious activity (rate limit triggers, repeated errors, etc.).
- **Incident Playbook:**
  - Document steps for responding to breaches, including key rotation and user notification.

---

## References
- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [Supabase Security Best Practices](https://supabase.com/docs/guides/auth)
- [FastAPI Security](https://fastapi.tiangolo.com/advanced/security/)
- [Next.js Security](https://nextjs.org/docs/advanced-features/security)

---

## Securing FastAPI Endpoints

Follow these steps to ensure your FastAPI endpoints are secure:

### 1. Use OAuth2/JWT Authentication
- Use FastAPI's built-in `OAuth2PasswordBearer` or integrate with Supabase Auth/JWT.
- Require a valid token for all protected endpoints:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validate JWT and extract user info
    ...
```

### 2. Enforce Role-Based Access Control (RBAC)
- Check user roles/permissions inside your endpoint dependencies:

```python
def require_admin(user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
```

### 3. Validate and Sanitize Input
- Use Pydantic models for all request bodies and query params.
- Add strict types and constraints (regex, enums, min/max, etc).

### 4. Prevent Injection Attacks
- Always use ORM or parameterized queries (never string interpolation).
- Sanitize all user input, especially in raw SQL or shell commands.

### 5. Enable CORS Properly
- Use FastAPI's CORS middleware:

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```
- Never use `*` for origins in production.

### 6. Rate Limiting & Abuse Protection
- Use a rate limiting library (e.g., `slowapi`, `fastapi-limiter`).
- Apply per-user and per-IP limits to sensitive endpoints.

### 7. Secure Error Handling
- Return generic error messages (no stack traces or sensitive info).
- Use FastAPI's exception handlers for consistent error responses.

### 8. Logging & Auditing
- Log all authentication, permission denials, and suspicious activity.
- Use structured logging and centralize logs for monitoring.

### 9. HTTPS & Secure Deployment
- Always deploy FastAPI behind HTTPS (use a reverse proxy like Nginx or Caddy).
- Set `secure` and `httponly` flags for cookies.
- Use environment variables for secrets.

### 10. Testing
- Write tests for authentication, permissions, and input validation.
- Use tools like pytest and httpx for API tests.

---

#### Example: Secure FastAPI Endpoint

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class Item(BaseModel):
    name: str
    description: str

@app.post("/items/")
def create_item(item: Item, token: str = Depends(oauth2_scheme)):
    # Validate token, check permissions, etc.
    ...
    return {"item": item}
```

---

For more details, see the [FastAPI Security Docs](https://fastapi.tiangolo.com/advanced/security/).

---

## TODO
- [ ] Regularly review and update this plan as the codebase evolves.
- [ ] Perform periodic penetration testing and threat modeling.
- [ ] Ensure all team members are trained on secure coding practices.

---

_Last updated: 2025-04-20_
