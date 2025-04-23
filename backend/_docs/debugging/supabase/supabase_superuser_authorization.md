# Debugging Supabase Superuser Authorization

## Issue Summary

When running `test_users_list_requires_superuser`, the test expects a `403 Forbidden` response for a normal user accessing `/api/v1/supabase/auth/admin/users`. Instead, it receives a `200 OK`, indicating that the endpoint is not correctly restricting access to superusers only.

## Test & Failure Evidence

- **Test:**
  - Calls endpoint as a normal user.
  - Expects: `response.status_code == 403`
  - Actual: `response.status_code == 200`

- **Key Log Evidence:**
  - Supabase API calls and user metadata updates are being made as expected.
  - User metadata for `is_superuser` is correctly set in Supabase for the superuser.
  - For the normal user, the JWT and metadata show `is_superuser: false`.
  - The endpoint still returns `200 OK` for a normal user.

- **Supabase API Responses:**
  - User creation for superuser: returns `422 email_exists` if user already exists, then proceeds to update metadata.
  - Metadata update: returns `200 OK`, and metadata is confirmed in Supabase.
  - Auth token and `/auth/v1/user` endpoint show correct metadata.

## Analysis

- The endpoint `/api/v1/supabase/auth/admin/users` is not enforcing the `is_superuser` check as expected, or the check is not working properly.
- The test helpers and fixtures are async-safe, and user metadata is being propagated and confirmed.
- The normal user is able to access the admin endpoint, which is a security issue.

## Next Steps

1. **Check Endpoint Authorization Logic:**
   - Ensure that the route for `/api/v1/supabase/auth/admin/users` is properly checking for `is_superuser` in the user's JWT/metadata.
   - Add debug logging in the route to print the user claims/roles at request time.

2. **Review Dependency Injection:**
   - Confirm that the dependency (e.g., `get_current_active_superuser`) is being used in the route and is correctly implemented.

3. **Retest After Fixes:**
   - After updating the endpoint logic, rerun the test to confirm that normal users receive a 403 and only superusers get 200.

## Open Questions

- Is the endpoint using the correct dependency to enforce superuser access?
- Is the JWT being decoded and checked for the correct claim?
- Are there any caching/session issues that could cause stale claims?

---

**Last updated:** 2025-04-23T16:58:59-06:00
