# Stripe Python SaaS Template

A complete Python template for building SaaS applications with Stripe integration. This template includes all essential functionality for subscription management, payment processing, customer management, and more.

## Features

### Core Stripe Integration
- **Customers**: Create, retrieve, update and delete Stripe customers
- **Products & Prices**: Manage your product catalog and pricing tiers
- **Subscriptions**: Handle subscription creation, updates, cancellations and renewals
- **Invoices & Billing**: Manage invoices, payment methods, and billing cycles
- **Customer Portal**: Allow customers to manage their own subscriptions
- **Connect**: Support for Stripe Connect for marketplace or platform businesses

### SaaS-Specific Features
- **Credit System**: Flexible credit/usage-based billing models
- **Metered Billing**: Support for metered subscriptions and usage tracking
- **Tiered Pricing**: Implementation of tiered pricing models
- **Trial Management**: Free trial setup and conversion

### Admin Functionality
- **Admin Dashboard**: Ready-to-customize admin interface
- **Reporting**: Revenue, customer, and subscription analytics
- **User Management**: Admin tools for managing users and permissions
- **Subscription Management**: Tools to manually adjust subscriptions

### Testing
- **Unit Tests**: Comprehensive test suite for all Stripe interactions
- **Mock Responses**: Pre-configured mock responses for Stripe API calls
- **Integration Tests**: End-to-end testing of payment flows

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/stripe-python-saas.git
cd stripe-python-saas

# Install required dependencies manually
pip install stripe
pip install django  # If using Django
```

## Configuration

Add your Stripe API keys to your environment or configuration file:

```python
# In your settings file
STRIPE_SECRET_KEY = "sk_test_..."
STRIPE_PUBLISHABLE_KEY = "pk_test_..."
```

## Quick Start

```python
# Initialize the Stripe client
from stripe_saas import StripeClient

client = StripeClient()

# Create a new customer
customer = client.customers.create(
    email="customer@example.com",
    name="Example Customer"
)

# Create a subscription
subscription = client.subscriptions.create(
    customer=customer.id,
    items=[{"price": "price_12345"}]
)
```

## Customer Portal Integration

The template includes ready-to-use integration with Stripe Customer Portal, allowing your users to manage their subscriptions directly:

```python
# Create a customer portal session
from stripe_saas.portal import create_portal_session

portal_session = create_portal_session(
    customer_id=customer.stripe_id,
    return_url="https://yourdomain.com/account"
)

# Redirect your customer to the portal URL
portal_url = portal_session.url
```

### Configuring the Customer Portal

```python
# Configure what customers can do in the portal
client.customer_portal.configurations.create(
    business_profile={
        "headline": "Your Company Subscription Management",
    },
    features={
        "subscription_update": {
            "enabled": True,
            "products": ["prod_12345", "prod_67890"],
        },
        "payment_method_update": {"enabled": True},
        "invoice_history": {"enabled": True},
    },
)
```

## Models

### Customer Model

```python
from stripe_saas.models import Customer

# Get or create a customer
customer, created = Customer.objects.get_or_create(
    email="customer@example.com",
    defaults={
        "name": "Example Customer"
    }
)

# Get the Stripe customer ID
stripe_customer_id = customer.stripe_id
```

### Subscription Model

```python
from stripe_saas.models import Subscription

# Get active subscriptions for a customer
active_subscriptions = Subscription.objects.filter(
    customer=customer,
    status='active'
)

# Check if customer has access to a feature
has_access = customer.has_feature_access('advanced_reporting')
```

### Credit Model

```python
from stripe_saas.models import CreditBalance

# Add credits to a customer account
CreditBalance.objects.add_credits(
    customer=customer,
    amount=100,
    description="Referral bonus"
)

# Use credits
CreditBalance.objects.use_credits(
    customer=customer,
    amount=10,
    feature="api_calls"
)
```

## Event Handling

This template provides event handler functions for important Stripe events. You can integrate these with your webhook endpoint implementation:

```python
from stripe_saas.events import handle_event

# Example usage in your webhook view
def webhook_endpoint(request):
    payload = request.body
    signature = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, signature, 'your_webhook_secret'
        )
        
        # Process the event using the template's handlers
        handle_event(event)
        
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)
```

The `handle_event` function processes events including:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.paid`
- `invoice.payment_failed`
- `charge.succeeded`
- `charge.failed`

## Signals

The template includes Django signals for key events:

```python
from stripe_saas.signals import subscription_created, subscription_updated

# Connect to the signals
@receiver(subscription_created)
def handle_new_subscription(sender, subscription, **kwargs):
    # Your custom logic here
    pass

@receiver(subscription_updated)
def handle_subscription_change(sender, subscription, **kwargs):
    # Your custom logic here
    pass
```

## Usage-Based Billing

```python
from stripe_saas.usage import report_usage

# Report usage for a metered subscription
report_usage(
    subscription_item_id="si_12345",
    quantity=1,
    timestamp=int(time.time())
)
```

## Tax Management

```python
# Set tax rates for a customer
client.customers.modify(
    customer.stripe_id,
    tax_id_data=[{"type": "eu_vat", "value": "DE123456789"}]
)

# Apply tax rates to a subscription
subscription = client.subscriptions.create(
    customer=customer.stripe_id,
    items=[{"price": "price_12345"}],
    default_tax_rates=["txr_12345"]
)
```

## Handling Failed Payments

```python
# Retrieve invoices with failed payments
failed_invoices = client.invoices.list(
    customer=customer.stripe_id,
    status="open"
)

# Attempt to pay a failed invoice
client.invoices.pay(failed_invoices[0].id)
```

## Refunds

```python
# Process a full refund
refund = client.refunds.create(
    charge="ch_12345"
)

# Process a partial refund
refund = client.refunds.create(
    charge="ch_12345",
    amount=1000  # $10.00
)
```

## Testing

The template includes a comprehensive testing suite:

```python
# Example test for subscription creation
def test_create_subscription(self):
    customer = self.create_test_customer()
    subscription = self.client.subscriptions.create(
        customer=customer.stripe_id,
        items=[{"price": self.test_price_id}]
    )
    self.assertEqual(subscription.status, "active")
```

For event handling testing:

```python
# Test event handling
def test_subscription_deleted_event(self):
    event_data = {
        "id": "evt_12345",
        "type": "customer.subscription.deleted",
        "data": {
            "object": {
                "id": "sub_12345",
                "customer": "cus_12345",
                "status": "canceled"
            }
        }
    }
    event = stripe.Event.construct_from(event_data, 'test_key')
    result = handle_event(event)
    self.assertTrue(result)
```

## Resources

- [Stripe API Documentation](https://docs.stripe.com/api)
- [Stripe Customer Portal](https://docs.stripe.com/billing/subscriptions/customer-portal)
- [Stripe Python Library](https://github.com/stripe/stripe-python)
- [Event Types Reference](https://docs.stripe.com/webhooks/webhook-events)

## License

MIT