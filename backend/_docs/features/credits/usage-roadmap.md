# Credits Usage Roadmap & Documentation

This document details how the credits system is designed, integrated, and used across the Lead Ignite backend. It includes technical implementation, integration patterns, and a roadmap for adoption and improvement.

---

## 1. Overview
- The credits system controls access to premium features and endpoints.
- Each user has a `credits_balance` in their `UserProfile`.
- Credits are deducted atomically when a user accesses a credit-consuming endpoint.
- All credit changes are logged in `CreditTransaction` for auditability.

## 2. Utility Function: `call_function_with_credits`
- A robust, type-annotated FastAPI utility for seamless integration with endpoints.
- Handles authentication, admin override, atomic deduction, error handling, and transaction logging.
- Usage pattern:
  ```python
  return await call_function_with_credits(
      my_endpoint_logic,
      request,
      db=db,
      current_user=current_user,
      credit_amount=5  # or dynamically determined
  )
  ```
- Endpoints that do NOT require credits should not use this wrapper, or pass `credit_amount=0`.

## 3. Endpoint Integration Table

| Endpoint                   | Credits Required | Notes                       |
|----------------------------|------------------|-----------------------------|
| `/api/v1/resourceA`        | 5                | Standard usage              |
| `/api/v1/resourceB`        | 0                | Free endpoint, no credits   |
| `/api/v1/resourceC`        | 10               | Admin override allowed      |
| `/api/v1/lead/export`      | 20               | Bulk export, high cost      |
| `/api/v1/lead/generate`    | 1                | Per-lead generation         |
| `/api/v1/user/profile`     | 0                | Account/profile management  |

> **Note:** Update this table as new endpoints are added or credit requirements change.

## 4. Selective Enforcement
- Use the utility only on endpoints that require credits.
- Document endpoints that are always free for clarity.
- Use a helper (e.g., `get_credit_cost`) to dynamically determine credits based on user tier, request data, or feature.

## 5. Error Handling & User Feedback
- If a user has insufficient credits, the endpoint returns HTTP 402 with a descriptive message (required, available, etc.).
- Credits are never deducted on failure.
- Admins can override the credit amount for testing or support.

## 6. Auditability
- All deductions/additions are recorded in `CreditTransaction`.
- Transactions are atomic to prevent race conditions or double-spending.

## 7. Stripe & Subscription Integration
- Credits are allocated on subscription creation/renewal (via Stripe webhook).
- Upgrades/downgrades adjust credits accordingly.
- All changes are logged for audit.

## 8. Testing & Quality
- Test coverage includes:
    - Users with 0, 1, exact, or more than required credits
    - Admin overrides
    - Edge cases (negative credits, invalid parameters)
    - Ensuring credits are not deducted on failure
- Tests should be non-flaky and revert any data changes.

## 9. Roadmap

### Immediate
- [x] Document all current endpoints and their credit requirements
- [x] Ensure all premium endpoints use the utility function
- [x] Add/expand tests for edge cases

### Short-Term
- [ ] Integrate credits usage into OpenAPI docs (endpoint descriptions, error responses)
- [ ] Add a decorator for even easier integration
- [ ] Centralize credits usage table in docs and keep it up to date

### Ongoing
- [ ] Regularly review endpoints for correct credits enforcement
- [ ] Update docs and tests as new features/endpoints are added
- [ ] Monitor audit logs for anomalies or abuse

---

_Last updated: 2025-04-20_

For implementation details, see `implmnentation.md` and `plan.md` in this folder.
