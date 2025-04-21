# Backend Security Roadmap for Lead Ignite

This roadmap outlines the actionable steps and priorities for securing the backend of the Lead Ignite platform, based on the current security plan and code audit findings.

---

## 1. Authentication & Authorization
- **Enforce JWT-based authentication** on all endpoints using Supabase Auth.
- **Role-Based Access Control (RBAC):** Ensure all sensitive endpoints check user roles (admin, agent, user, etc.).
- **Row-Level Security (RLS):** Use Supabase/Postgres RLS to restrict data access to resource owners.
- **OAuth:** Use secure OAuth flows for external integrations, never exposing client secrets.

## 2. Input Validation & Sanitization
- **Strict Pydantic validation** for all request payloads.
- **Sanitize all user input** (prevent XSS, SQL injection, etc.).
- **Enforce strong typing** (e.g., EmailStr, constr for regex fields).

## 3. Rate Limiting & Abuse Prevention
- **Implement FastAPI-limiter** (or similar) middleware to protect all endpoints, especially auth and public endpoints.
- **Brute force protection:** Lock accounts or require CAPTCHA after repeated failed login attempts.

## 4. Secrets & Sensitive Data
- **Store all secrets in environment variables** or a secret manager (never in code or git).
- **Rotate tokens and secrets** regularly.

## 5. Error Handling & Logging
- **Consistent error responses:** Never leak stack traces or sensitive info in API errors.
- **Centralized logging:** Log all auth events, permission denials, and suspicious activity with user/IP/timestamp.

## 6. CORS & CSRF
- **CORS:** Only allow trusted origins in production.
- **CSRF:** Use anti-CSRF tokens or double-submit cookies for state-changing endpoints.

## 7. Security Headers & Best Practices
- **Add security headers** (X-Content-Type-Options, X-Frame-Options, Strict-Transport-Security, etc.).
- **Validate file uploads:** Check type and size.
- **Document security controls** in OpenAPI docs.

---

## Implementation Notes (from Audit & Prompt)
- All sensitive endpoints already require authentication and proper role checks.
- Pydantic models are used for validation; ensure all fields are properly typed and sanitized.
- No explicit rate limiting found—add FastAPI-limiter middleware.
- Error handling is generic, but ensure no stack traces or sensitive data leak in production.
- CORS is enabled, but review allowed origins for strictness.
- Use .env and never commit secrets; prefer a secret manager in production.
- Log all permission denials and suspicious activity.
- Add security headers middleware for additional protection.

---

## Milestones
1. **Immediate:**
   - Audit and patch any endpoints missing Depends for authentication/authorization. ✅ Completed
   - Add FastAPI-limiter middleware. ⏳ In Progress
   - Review CORS origins and restrict in production. ✅ Completed
   - Add security headers middleware. ⏳ In Progress
2. **Short-Term:**
   - Integrate centralized logging and anomaly monitoring.
   - Implement brute force protection for login endpoints.
   - Harden file upload validation.
3. **Ongoing:**
   - Regularly review dependencies for vulnerabilities.
   - Rotate secrets and tokens.
   - Update documentation and OpenAPI specs.

---

## References
- See `security-plan.md` for detailed policy.
- See code audit notes above for specific recommendations.
