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
@csrf_exempt
def my_webhook_view(request):
  webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
  request_data = json.loads(request.data)

  if webhook_secret:
      return HttpResponse('Webhook secret yo!')

      # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
      signature = request.headers.get('stripe-signature')
      try:
          event = stripe.Webhook.construct_event(
              payload=request.data, sig_header=signature, secret=webhook_secret)
          data = event['data']
      except Exception as e:
          return e
      # Get the type of webhook event sent - used to check the status of PaymentIntents.
      event_type = event['type']
  else:
      return HttpResponse('Not getting webhook secret yo!')
      data = request_data['data']
      event_type = request_data['type']

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