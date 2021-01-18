import os
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, permissions

from rest_framework import generics
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist 
import json
from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from subscription.models import Subscription, InvoiceId,StripeSubscription, SUBSCRIPTION_PROFILES
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import time
from items.models import Item
from containers.models import Container
# Using Django
# newest version
import stripe
stripe.api_key = os.getenv('STRIPE_API_SECRET')



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
        invoiceId=(data['object']['id'])

        subId=(data['object']['subscription'])
        #check against priceIds and prices to find out if we should do a full refill or a partial refill

        try:
            if not data['object']['status'] =='paid':
                return JsonResponse('Invoice status is not paid!',status=400,safe=False)
            if data['object']['amount_paid']==0:
                return JsonResponse('Invoice generated due to downgrade', safe=False)
            stripeSub=StripeSubscription.objects.get(stripeSubscriptionId=str(subId))

            stripeSub.subscription.subscriptionUpdateInProgress=False
            stripeSub.subscription.save()

            # should be a totally indepedent invoice
            # refill and refresh subscriptionType (), refill time
            if data['object']['lines']['total_count']==1:
                stripeSub.subscription.initialize_or_refill(data['object']['lines']['data'][0]['plan']['product'])
                # this may be overly simplistic
                stripeSub.currentPeriodEnd=data['object']['lines']['data'][0]['period']['end']
                stripeSub.save()
            # should be an update (upgrade/downgrade to subscription)
            # upgrade (incrementing totalRequest allowed ect) if upgrade and updata subscriptionType
            elif data['object']['lines']['total_count']==2:
                # this is a pretty dumb way to do it (no documentation) but should work
                invoice1=data['object']['lines']['data'][0]
                invoice2=data['object']['lines']['data'][1]
                if (invoice1['amount']<0 and invoice2['amount']<0) or (invoice1['amount']>0 and invoice2['amount']>0):
                    raise Exception("unknown case where there are 2 positive or 2 negative prices")
                # pass the product_id to the subscription
                if invoice1['amount']>0:

                    stripeSub.subscription.initialize_or_refill(invoice1['plan']['product'])
                    # this may be overly simplistic
                    stripeSub.currentPeriodEnd=invoice1['period']['end']
                    stripeSub.save()
                else:
                    stripeSub.subscription.initialize_or_refill(invoice2['plan']['product'])
                    # this may be overly simplistic
                    stripeSub.currentPeriodEnd=invoice2['period']['end']
                    stripeSub.save()
            else:
                raise Exception("unknown case where there are 3 or more subscriptions")
            #foundSub=[subscription for subscription in SUBSCRIPTION_PROFILES if subscription[2]==subId]
        except StripeSubscription.DoesNotExist:
                return JsonResponse('Couldnt find the subscription. Invoice not paid!',status=400,safe=False)
        except:
            return JsonResponse('Invoice not paid!',status=400,safe=False)
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.

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
    sub.subscriptionUpdateInProgress=False

    stripeSubscriptions=StripeSubscription.objects.filter(subscription=sub).order_by('-created')
    if len(stripeSubscriptions)>0:
        if stripeSubscriptions[0].deleted==False:
            return JsonResponse("You already have a subscription",status=400,safe=False)
    stripeCustomerId=sub.stripeCustomerId
    data = request.data
    # Attach the payment method to the customer
    try:
        stripe.PaymentMethod.attach(
            data['paymentMethodId'],
            customer=stripeCustomerId,
        )
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        return JsonResponse(str(e.user_message), status=500, safe=False)
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        return JsonResponse("Too many requests made to our payment system too quickly. Please wait and try again.", status=500, safe=False)
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        return JsonResponse("InvalidRequestError.", status=500, safe=False)
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        return JsonResponse("Contact support. Error code 1", status=500, safe=False)
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        return JsonResponse("Contact support. Error code 2", status=500, safe=False)
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        return JsonResponse("Contact support. Error code 3", status=500, safe=False)
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        return JsonResponse("Contact support. Error code 4", status=500, safe=False)
    # Set the default payment method on the customer
    try:
        stripe.Customer.modify(
            stripeCustomerId,
            invoice_settings={
                'default_payment_method': data['paymentMethodId'],
            },
        )
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        return JsonResponse(str(e.user_message), status=500, safe=False)
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        return JsonResponse("Too many requests made to our payment system too quickly. Please wait and try again.", status=500, safe=False)
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        return JsonResponse("InvalidRequestError.", status=500, safe=False)
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        return JsonResponse("Contact support. Error code 5", status=500, safe=False)
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        return JsonResponse("Contact support. Error code 6", status=500, safe=False)
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        return JsonResponse("Contact support. Error code 7", status=500, safe=False)
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        return JsonResponse("Contact support. Error code 8", status=500, safe=False)

    # Create the subscription
    try:
        subscription = stripe.Subscription.create(
            customer=stripeCustomerId,
            items=[
                {
                    'price': data['priceId']
                }
            ],
            expand=['latest_invoice.payment_intent'],
            payment_behavior='error_if_incomplete',

        )
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        return JsonResponse(str(e.user_message), status=500, safe=False)
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        return JsonResponse("Too many requests made to our payment system too quickly. Please wait and try again.", status=500, safe=False)
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        return JsonResponse("InvalidRequestError.", status=500, safe=False)
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        return JsonResponse("Contact support. Error code 9", status=500, safe=False)
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        return JsonResponse("Contact support. Error code 10", status=500, safe=False)
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        return JsonResponse("Contact support. Error code 11", status=500, safe=False)
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        return JsonResponse("Contact support. Error code 12", status=500, safe=False)
    sub.subscriptionUpdateInProgress=True

    # need to store fields here; such as id, items.data.price.id,customer,currentPeriodEnd
    

    newStripeSubscription=StripeSubscription(subscription=sub
    ,createdStripe=subscription['created']
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
def retry_invoice(request):
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
    try:
        invoiceIdsSorted=InvoiceId.objects.filter(stripeSubscription=stripeSubscription).order_by('-created')
        foundInvoiceId=invoiceIdsSorted[0].stripeInvoiceId
        invoice = stripe.Invoice.retrieve(
            foundInvoiceId,
            expand=['payment_intent'],
        )
        return JsonResponse(invoice)
    except:
        return JsonResponse("No invoice has gone through yet",safe=False)

@api_view(['get'])
@permission_classes([permissions.IsAuthenticated])
def get_subscription_info(request):
    try:
        sub=Subscription.objects.get(owner=request.user)
        stripeSubscriptions=StripeSubscription.objects.filter(subscription=sub).order_by('-created')

        subscriptionActive=False
        returnData={}

        if len(stripeSubscriptions)>0:
            returnData['subscriptionExpirationTime']=stripeSubscriptions[0].currentPeriodEnd

            if stripeSubscriptions[0].deleted==False:
                subscriptionActive=True
                # these fields must be initialized
                returnData['paymentExpired']=stripeSubscriptions[0].currentPeriodEnd>(time.time())
        else:
            if sub.subscriptionType=='trial':
                returnData['subscriptionExpirationTime']=str(sub.created.timestamp()+(60*60*24*14))
            else:
                returnData['subscriptionExpirationTime']='null'

        if not subscriptionActive:
            returnData['paymentExpired']='null'
        # corresponds to ability to change subscription vs. ability to create subscription
        returnData['subscriptionActive']=subscriptionActive
        # 2 day grace period applied to userViewRights and also all remaining subscription time after a cancel
        returnData['paymentUpToDate']=sub.getPaymentUpToDate()
        returnData['subscriptionType']=sub.subscriptionType
        returnData['shipmentsAllowed']=sub.shipmentsAllowed
        returnData['shipmentsUsed']=sub.shipmentsUsed
        returnData['itemsAllowed']=sub.itemsAllowed
        returnData['itemsUsed']=sub.getItemsUsed()
        returnData['containersAllowed']=sub.containersAllowed
        returnData['containersUsed']=sub.getContainersUsed()
        returnData['subscriptionUpdateInProgress']=sub.subscriptionUpdateInProgress
        return JsonResponse(returnData)
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
        return JsonResponse(str(e),status=403, safe=False)

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
        upgrade= sub.choose_upgrade_or_downgrade_with_price_id(data['priceId'])
        if upgrade:
            sub.subscriptionUpdateInProgress=False
            try:
                updatedSubscription = stripe.Subscription.modify(
                    stripeSubscriptionId,
                    cancel_at_period_end=False,
                    items=[{
                        'id': fetchedSubscription['items']['data'][0].id,
                        'price': data['priceId'],
                    }],

                    # this should be none if we are downgrading
                    proration_behavior='always_invoice',
                    # attempt to set proration_date to start of the current period (this billing cycle) so no matter
                    # when you upgrade it has the same cost
                    proration_date=fetchedSubscription['current_period_start'],
                    billing_cycle_anchor='now',
                    payment_behavior='error_if_incomplete',
                )

            except stripe.error.CardError as e:
                # Since it's a decline, stripe.error.CardError will be caught
                return JsonResponse(str(e.user_message), status=500, safe=False)
            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                return JsonResponse("Too many requests made to our payment system too quickly. Please wait and try again.", status=500, safe=False)
            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                return JsonResponse("InvalidRequestError.", status=500, safe=False)
            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                return JsonResponse("Contact support. Error type 1", status=500, safe=False)
            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                return JsonResponse("Contact support. Error type 2", status=500, safe=False)
            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                return JsonResponse("Contact support. Error type 3", status=500, safe=False)
            except Exception as e:
                # Something else happened, completely unrelated to Stripe
                return JsonResponse("Contact support. Error type 4", status=500, safe=False)

            sub.subscriptionUpdateInProgress=True

        else:
            try:
                updatedSubscription = stripe.Subscription.modify(
                    stripeSubscriptionId,
                    cancel_at_period_end=False,
                    items=[{
                        'id': fetchedSubscription['items']['data'][0].id,
                        'price': data['priceId'],
                    }],

                    # this should be none if we are downgrading
                    proration_behavior='none',
                    payment_behavior='error_if_incomplete',

                    # attempt to set proration_date to start of the current period (this billing cycle) so no matter
                    # when you upgrade it has the same cost
                )
            except Exception as e:
                return JsonResponse("Contact support. Error canceling subscription.", status=500, safe=False)

            sub.downgrade_subscription(data['priceId'])

        return JsonResponse(updatedSubscription)
    except Exception as e:
        return JsonResponse(str(e),status=403, safe=False)


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