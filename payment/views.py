import os
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, permissions

from rest_framework import generics
from django.shortcuts import render
import json
from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from subscription.models import Subscription, InvoiceId,StripeSubscription
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Using Django
# newest version
import stripe
stripe.api_key = 'sk_test_51HB4dCJWFTMXIZUo5d1tlWus4t0NGBLPI6LqHVokCzOyXaYZ6f8rcBqAeWZUdtfdc6tl5EenjpUXWrpFsyRmAwgJ00fRuOxc8b'
# dont know where this should be set
os.environ["STRIPE_WEBHOOK_SECRET"] = "whsec_VtPsqS18E3v6S5vDeEgXg5FDlYZdSYHV"
# spurious commit


@csrf_exempt
@api_view(['POST'])
def my_webhook_view(request):
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = request.body
    if webhook_secret:

        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.META['HTTP_STRIPE_SIGNATURE']
        try:
            event = stripe.Webhook.construct_event(
                payload=request_data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return JsonResponse('Couldnt authenticate payment credentials', status=400, safe=False)
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']

    else:
        data = request.data
        event_type = request.method
        # couldnt authenticate
        return JsonResponse('Couldnt authenticate payment credentials', status=400, safe=False)

    data_object = data['object']
    # this may eventually be too slow!!!!!!!
    if event_type == 'invoice.created':
        invoiceId=(data['object']['id'])
        subId=(data['object']['subscription'])
        try:
            stripeSub=StripeSubscription.objects.get(stripeSubscriptionId=str(subId))
            invoiceIdObject=InvoiceId(stripeSubscription=stripeSub, stripeInvoiceId=str(invoiceId))
            invoiceIdObject.save()
            return JsonResponse('Invoice created yo !'+str(invoiceId),safe=False)
        except:
            return JsonResponse('Invoice created; too slow or couldnt find unique subscription',safe=False)
    if event_type == 'invoice.paid':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.

        # will need to check against priceIds and prices to find out if we should do a full refill or a partial refill
        return JsonResponse('Invoice paid yo!', safe=False)

    if event_type == 'invoice.payment_failed':
        # If the payment fails or the customer does not have a valid payment method,
        # an invoice.payment_failed event is sent, the subscription becomes past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        return JsonResponse('Payment failed yo!', safe=False)

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

    return JsonResponse({'status': 'success'})


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
# note: this is not the same as updating subscription, stripe subscription is a field
# in subscription, has different permissions (needs to be exposed to the nonuser that is webhook)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'paymentMethodId': openapi.Schema(type=openapi.TYPE_STRING),
        'priceId': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(['post'])
@permission_classes([permissions.IsAuthenticated])
def create_stripe_subscription(request):
    sub = Subscription.objects.get(owner=request.user)
    stripeSubscriptions=StripeSubscription.objects.filter(subscription=sub).order_by('-created')
    if len(stripeSubscriptions)>0:
        if stripeSubscriptions[0].deleted==False:
            return JsonResponse("You already have a subscription",safe=False, code=400)
    stripeCustomerId=sub.stripeCustomerId
    data = request.data
    # Attach the payment method to the customer
    stripe.PaymentMethod.attach(
        data['paymentMethodId'],
        customer=stripeCustomerId,
    )
    # Set the default payment method on the customer
    stripe.Customer.modify(
        stripeCustomerId,
        invoice_settings={
            'default_payment_method': data['paymentMethodId'],
        },
    )

    # Create the subscription
    subscription = stripe.Subscription.create(
        customer=stripeCustomerId,
        items=[
            {
                'price': data['priceId']
            }
        ],
        expand=['latest_invoice.payment_intent'],
    )
    # need to store fields here; such as id, items.data.price.id,customer,currentPeriodEnd
    

    newStripeSubscription=StripeSubscription(subscription=sub
    ,stripeSubscriptionId=subscription['id']
    ,stripeSubscriptionItemDataPriceId=subscription['items']['data'][0]['price']['id']
    ,stripeSubscriptionCustomer=subscription['customer'])
    newStripeSubscription.save()

    return JsonResponse(subscription)
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'paymentMethodId': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(['post'])
@permission_classes([permissions.IsAuthenticated])
def retry_stripe_subscription(request):
    sub = Subscription.objects.get(owner=request.user)
    
    stripeCustomerId=sub.stripeCustomerId

    data = request.data

    stripe.PaymentMethod.attach(
        data['paymentMethodId'],
        customer=stripeCustomerId,
    )
    # Set the default payment method on the customer
    stripe.Customer.modify(
        stripeCustomerId,
        invoice_settings={
            'default_payment_method': data['paymentMethodId'],
        },
    )

    stripeSubscription=StripeSubscription.objects.filter(subscription=sub).order_by('-created')[0]
    #TODO: fix possibility to bug out here
    invoiceIdsSorted=InvoiceId.objects.filter(stripeSubscription=stripeSubscription).order_by('-created')
    foundInvoiceId=invoiceIdsSorted[0].stripeInvoiceId
    invoice = stripe.Invoice.retrieve(
        foundInvoiceId,
        expand=['payment_intent'],
    )
    return JsonResponse(invoice)

@api_view(['get'])
@permission_classes([permissions.IsAuthenticated])
def user_has_stripe_subscription(request):
    try:
        sub=Subscription.objects.get(owner=request.user)
        stripeSubscriptions=StripeSubscription.objects.filter(subscription=sub)

        subscriptionActive=False
        if len(stripeSubscriptions)>0:
            if stripeSubscriptions.order_by('-created')[0].deleted==False:
                subscriptionActive=True

        return JsonResponse({'subscriptionActive': subscriptionActive})
    except:
        return JsonResponse('Error getting this info',safe=False)


@api_view(['delete'])
@permission_classes([permissions.IsAuthenticated])
def cancel_subscription(request):
    try:
        sub=Subscription.objects.get(owner=request.user)
        stripeSub=StripeSubscription.objects.filter(subscription=sub).order_by('-created')[0]
         # Cancel the subscription by deleting it
        deletedSubscriptionData = stripe.Subscription.delete(stripeSub.stripeSubscriptionId)
        stripeSub.deleted=True
        stripeSub.save()
        return JsonResponse(deletedSubscriptionData)
    except Exception as e:
        return JsonResponse(str(e),code=403, safe=False)

@swagger_auto_schema(method='put', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'priceId': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(['put'])
@permission_classes([permissions.IsAuthenticated])
#this relies upon invoice.paid distinguishing between full and partial refills of user requests
def update_stripe_subscription(request):
    data = request.data
    try:
        sub=Subscription.objects.get(owner=request.user)
        stripeSub=StripeSubscription.objects.filter(subscription=sub).order_by('-created')[0]
        stripeSubscriptionId=stripeSub.stripeSubscriptionId

        fetchedSubscription = stripe.Subscription.retrieve(stripeSubscriptionId)

        updatedSubscription = stripe.Subscription.modify(
            stripeSubscriptionId,
            cancel_at_period_end=False,
            items=[{
                'id': fetchedSubscription['items']['data'][0].id,
                'price': data['priceId'],
            }]
        )
        return JsonResponse(updatedSubscription)
    except Exception as e:
        return JsonResponse(str(e),code=403, safe=False)


'''
@api_view(['get'])
@permission_classes([permissions.IsAuthenticated])
def user_subscription(request):
    try:
        sub=Subscription.objects.get(owner=request.user)
        stripeSubIsNull=(sub.stripeSubscriptionId=='null')
        print(stripeSubIsNull)

        if stripeSubIsNull:
            return JsonResponse({'id':stripeSubIsNull})
        else:
            # Create the subscription
            subscription = stripe.Subscription.retrieve(
                id=sub.stripeSubscriptionId,
                expand=['latest_invoice.payment_intent'],
            )
            return JsonResponse(subscription)

    except:
        return JsonResponse('Error getting this info',safe=False)
'''