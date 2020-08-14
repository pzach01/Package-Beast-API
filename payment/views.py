from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status


from django.shortcuts import render
import json
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Using Django
# newest version
import stripe
stripe.api_key = 'sk_test_51HB4dCJWFTMXIZUo5d1tlWus4t0NGBLPI6LqHVokCzOyXaYZ6f8rcBqAeWZUdtfdc6tl5EenjpUXWrpFsyRmAwgJ00fRuOxc8b'
import os
# dont know where this should be set
os.environ["STRIPE_WEBHOOK_SECRET"] = "whsec_VtPsqS18E3v6S5vDeEgXg5FDlYZdSYHV"
# spurious commit
@csrf_exempt
@api_view(['POST'])
def my_webhook_view(request):
  webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
  request_data = request.body
  webhook_secret=False
  if webhook_secret:

      # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
      signature= request.META['HTTP_STRIPE_SIGNATURE']
      try:
          event = stripe.Webhook.construct_event(
              payload=request_data, sig_header=signature, secret=webhook_secret)
          data = event['data']
      except Exception as e:
        return HttpResponse('Couldnt authenticate payment credentials', status=400)
      # Get the type of webhook event sent - used to check the status of PaymentIntents.
      event_type = event['type']
      return HttpResponse('Webhook secret worked yo!')

  else:
      data = request.data
      event_type = request.method
      # couldnt authenticate
      return HttpResponse('Couldnt authenticate payment credentials', status=400)

  data_object = data['object']

  if event_type == 'invoice.paid':
      # Used to provision services after the trial has ended.
      # The status of the invoice will show up as paid. Store the status in your
      # database to reference when a user accesses your service to avoid hitting rate
      # limits.
      print(data)

  if event_type == 'invoice.payment_failed':
      # If the payment fails or the customer does not have a valid payment method,
      # an invoice.payment_failed event is sent, the subscription becomes past_due.
      # Use this webhook to notify your user that their payment has
      # failed and to retrieve new card details.
      print(data)

  if event_type == 'invoice.finalized':
      # If you want to manually send out invoices to your customers
      # or store them locally to reference to avoid hitting Stripe rate limits.
      print(data)

  if event_type == 'customer.subscription.deleted':
      # handle subscription cancelled automatically based
      # upon your subscription settings. Or if the user cancels it.
      print(data)

  if event_type == 'customer.subscription.trial_will_end':
      # Send notification to your user that the trial will end
      print(data)

  return jsonify({'status': 'success'})