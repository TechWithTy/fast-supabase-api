# Supabase Email Confirmation Debugging Context

This document summarizes the debugging process and findings regarding persistent email confirmation issues with Supabase user authentication.

## Problem Statement
- Supabase continued to require email confirmation for new users, even after disabling the "Confirm email" setting in the dashboard.
- New users appeared in the dashboard as "Waiting for verification" and API responses included `email_not_confirmed` errors.

## Debugging Steps & Insights
1. **Verified Supabase Auth Settings:**
   - Confirmed that "Confirm email" was toggled off in the Supabase dashboard under Authentication > Settings > Email Auth.
2. **Tested with New Emails:**
   - Tried signing up with new, never-used emails. Still received `email_not_confirmed` errors and users remained unconfirmed.
3. **Checked Project Reference:**
   - Ensured that the backend was using the correct Supabase project URL and anon/public key.
4. **Waited for Setting Propagation:**
   - Allowed several minutes for dashboard setting changes to propagate. No change in behavior.
5. **Manual User Deletion:**
   - Deleted test users from the dashboard and attempted to sign up again. Still resulted in unconfirmed users.
6. **Manual User Confirmation:**
   - Manually confirming users in the dashboard allowed sign-in, but this is not a scalable solution for automated testing.
7. **Considered Custom Auth Hooks:**
   - Verified that no custom auth hooks or email templates were enforcing confirmation.

## Potential Root Causes
- **Supabase dashboard setting not propagating properly.**
- **Backend using incorrect project or keys.**
- **Supabase bug or regional service delay.**
- **Custom logic overriding default behavior (not present in this case).**

## Workarounds & Recommendations
- Double-check project reference and keys in backend configuration.
- Toggle the "Confirm email" setting on/off and save again.
- Wait several minutes after changing settings before testing.
- Use a brand new email for each test attempt.
- As a last resort, manually confirm users in the dashboard or use the Supabase Admin API to patch users as confirmed.
- If none of these resolve the issue, contact Supabase support or check for platform-wide issues.

## Example: Programmatic User Confirmation (Admin API)
```python
import requests
from datetime import datetime

SUPABASE_URL = "https://YOUR_PROJECT_REF.supabase.co"
SERVICE_ROLE_KEY = "YOUR_SERVICE_ROLE_KEY"
user_id = "the-user-id-from-signup"

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
}
data = {"email_confirmed_at": datetime.utcnow().isoformat()}
resp = requests.patch(f"{SUPABASE_URL}/auth/v1/admin/users/{user_id}", headers=headers, json=data)
```

## Pending Test Failures Due to Supabase Email Rate Limiting

- As of April 2025, automated and manual tests that depend on user email confirmation (e.g., test_users_authorization.py) are failing due to Supabase email rate limiting and/or SMTP restrictions.
- Even after switching to a custom SMTP provider (SendGrid), Supabase's internal rate limits and/or project restrictions can prevent all transactional emails (including confirmation and recovery emails) from being sent.
- This results in users remaining unconfirmed, and tests that require a confirmed user will fail with errors like `email_not_confirmed`.
- A support ticket has been submitted to Supabase requesting a review and lifting of these restrictions. Until support responds and restores email functionality, these tests will remain in a failing state.
- Comments have been added to relevant test files to document this dependency and the external blocker.

### Error Example

```
Failed to send password recovery: failed to make recover request: email rate limit exceeded
```

### Next Steps
- Monitor support ticket and update documentation/tests once email sending is restored.
- Use manual user confirmation for critical testing if needed.
- Avoid repeated test signups/resets to prevent further rate limiting.

---

**If this issue persists after all checks, it is likely a Supabase platform bug or propagation delay.**
