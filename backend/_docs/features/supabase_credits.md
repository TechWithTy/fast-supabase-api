# Supabase Credits System Documentation

This document describes the credits system implemented in the Supabase backend, covering **AI Credits**, **Lead Credits**, and **Skip Trace Credits**. Each credit type is managed in its own table and linked to user subscriptions for granular access control and billing.

---

## AI Credits
**Table:** `AICredits`

- **Purpose:** Tracks credits for AI-powered features (e.g., AI enrichment, analysis, or automation).
- **Key Columns:**
  - `id` (uuid): Primary key
  - `allotted` (int): Number of AI credits assigned
  - `used` (int): Number of AI credits consumed
  - `resetindays` (int): Days until credits reset
  - `subscriptionid` (uuid): Foreign key to `UserProfileSubscription.id`
- **Usage:**
  - Credits are deducted when AI features are used.
  - Resets can be scheduled based on `resetindays`.

---

## Lead Credits
**Table:** `LeadCredits`

- **Purpose:** Tracks credits for lead generation or acquisition features.
- **Key Columns:**
  - `id` (uuid): Primary key
  - `allotted` (int): Number of lead credits assigned
  - `used` (int): Number of lead credits consumed
  - `resetindays` (int): Days until credits reset
  - `subscriptionid` (uuid): Foreign key to `UserProfileSubscription.id`
- **Usage:**
  - Credits decrease as leads are generated or exported.
  - Resets are handled according to the subscription plan.

---

## Skip Trace Credits
**Table:** `SkipTraceCredits`

- **Purpose:** Tracks credits for skip tracing services (finding contact info, etc.).
- **Key Columns:**
  - `id` (uuid): Primary key
  - `allotted` (int): Number of skip trace credits assigned
  - `used` (int): Number of skip trace credits consumed
  - `resetindays` (int): Days until credits reset
  - `subscriptionid` (uuid): Foreign key to `UserProfileSubscription.id`
- **Usage:**
  - Credits are deducted as skip trace lookups are performed.
  - Resets are scheduled per subscription cycle.

---

## Relationships & Best Practices
- All credit tables are linked to a subscription (`UserProfileSubscription`) via a UUID foreign key.
- Credits are managed per subscription, allowing for flexible plans and renewals.
- Always ensure the `subscriptionid` is valid and references an existing subscription.
- Use atomic operations for credit deduction to prevent race conditions.

---

## Example SQL for Adding Credits
```sql
INSERT INTO "AICredits" (id, allotted, used, resetindays, subscriptionid)
VALUES (gen_random_uuid(), 100, 0, 30, '<SUBSCRIPTION_UUID>');

INSERT INTO "LeadCredits" (id, allotted, used, resetindays, subscriptionid)
VALUES (gen_random_uuid(), 50, 0, 30, '<SUBSCRIPTION_UUID>');

INSERT INTO "SkipTraceCredits" (id, allotted, used, resetindays, subscriptionid)
VALUES (gen_random_uuid(), 25, 0, 30, '<SUBSCRIPTION_UUID>');
```
Replace `<SUBSCRIPTION_UUID>` with the actual subscription UUID.

---

## See Also
- [UserProfileSubscription Table Schema](#)
- [Supabase Auth Users](#)
- [API Endpoints for Credits Management](#)
