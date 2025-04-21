from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
def invoice_deleted_webhook(request):
    payload = json.loads(request.body)
    
    # Extract relevant information from the payload
    invoice_id = payload.get('_id')
    status = payload.get('status')
    invoice_number = payload.get('invoiceNumber')
    amount_due = payload.get('amountDue')
    
    # Process the deleted invoice
    # Add your business logic here, e.g., updating database, sending notifications, etc.
    
    # Example: Print some information about the deleted invoice
    print(f"Invoice {invoice_number} (ID: {invoice_id}) has been deleted.")
    print(f"Status: {status}")
    print(f"Amount due: {amount_due}")
    
    # Return a success response
    return HttpResponse("Webhook received successfully", status=200)