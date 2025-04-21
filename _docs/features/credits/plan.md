Credit Balance & Deduction
UserProfile Model
Each user has a credits_balance field in their UserProfile.
Deduction Utility
The main method for deducting credits is:
python
CopyInsert
@transaction.atomic
def deduct_credits(self, amount: int) -> bool:
    """
    Deduct credits from the user's balance with transaction safety.
    Uses select_for_update to lock the row during transaction, preventing race conditions.
    Returns True if successful, False if insufficient credits.
    """
    user_profile = UserProfile.objects.select_for_update().get(id=self.id)
    if user_profile.has_sufficient_credits(amount):
        user_profile.credits_balance -= amount
        user_profile.save(update_fields=['credits_balance', 'updated_at'])
        self.credits_balance = user_profile.credits_balance
        self.updated_at = user_profile.updated_at
        return True
    return False
This ensures only users with enough credits can use credit-consuming endpoints.
The check for sufficient credits is done with has_sufficient_credits(required_credits: int) -> bool.
2. Minimum Credits Enforcement
Endpoints
Many endpoints require a minimum number of credits to execute.
Example from tests:
python
CopyInsert
assert response.data['required'] == 5  # Default credit cost
If the user has insufficient credits, the endpoint returns HTTP 402 with an error message.
3. Utility Function for Credit Use
call_function_with_credits
Endpoints often use a utility function to wrap their logic, handling deduction and enforcement:
python
CopyInsert
return call_function_with_credits(
    self.perform_get,
    request,
    credit_cost=self.get_credit_cost(request)
)
get_credit_cost can dynamically determine the cost based on user tier/plan.
If the user has enough credits, the wrapped function is called and credits are deducted.
If not, an error is returned and no credits are deducted.
4. Credit Transactions & Recording
CreditTransaction Model
All credit changes (deductions and additions) are recorded for auditability.
This is done atomically to ensure consistency.
5. Integration with Subscriptions
Stripe Integration
Credits are allocated on subscription creation and renewal, with tier-based amounts.
Upgrades/downgrades adjust credits accordingly.
All changes are recorded in CreditTransaction.
6. Testing
Test Coverage
There are tests for:
Users with 0, 1, exact, or more than required credits.
Admin overrides.
Edge cases (negative credits, invalid parameters).
Ensuring credits are not deducted on failure.
Summary Table
| Feature | Implementation Detail | |--------------------------|-----------------------------------------------------------------------| | Deduct credits | UserProfile.deduct_credits(amount) | | Minimum credits to use | Enforced per endpoint, usually 5 by default (can be dynamic) | | Utility function | call_function_with_credits wraps endpoint logic | | Transaction recording | CreditTransaction model, atomic operations | | Stripe integration | Credits allocated/adjusted on subscription events | | Tests | Cover insufficient, exact, admin, and edge cases |