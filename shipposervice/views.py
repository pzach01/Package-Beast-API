from django.shortcuts import render


import os

from rest_framework import generics, viewsets, permissions
import requests
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from users.models import User
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from shipposervice.models import ShippoRefund, ShippoTransaction, ShippoMessage
from shipposervice.serializers import ShippoTransactionSerializer, ShippoRefundSerializer
from quotes.models import Quote
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'rateId': openapi.Schema(type=openapi.TYPE_STRING),
        'labelFileType': openapi.Schema(type=openapi.TYPE_STRING),

    }
))

@api_view(['post'])
@permission_classes([permissions.IsAuthenticated,IsOwner])
def generate_shippo_transaction(request):
    import shippo

    user=User.objects.get(email=request.user)
    if user.userHasShippoAccount() and (os.getenv('ENVIRONMENT_TYPE')=='PRODUCTION'):
        shippo.config.api_key=user.shippoAccessToken
    else:
        shippo.config.api_key = os.getenv('SHIPPO_API_KEY')

    rateId=request.data['rateId']
    labelFileType=request.data['labelFileType']
    foundQuote=None
    try:
        foundQuote=Quote.objects.filter(owner=request.user).filter(shippoRateId=rateId)[0]
    except:
        return JsonResponse('Couldnt find rate in generate_shippo_transaction',safe=False,status=400)
    try:
        ShippoTransaction.objects.get(quote=foundQuote)
        return JsonResponse('This quote already has a shippo transaction',safe=False,status=400)
    except ObjectDoesNotExist:
        pass
    except ShippoTransaction.MultipleObjectsReturned:
        return JsonResponse('This quote already has created multiple shippo transactions, contact admin',safe=False,status=400)
    transaction = shippo.Transaction.create( 
        rate=rateId, 
        label_file_type=labelFileType, 
        asynchronous=False)
    shippoTransaction=ShippoTransaction.objects.create(owner=request.user,label_url=transaction['label_url'],quote=foundQuote)
    if "messages" in transaction:
        for message in transaction['messages']:
            ShippoMessage.objects.create(shippoTransaction=shippoTransaction, **message)
    shippoTransaction.objectState=transaction['object_state']
    shippoTransaction.status=transaction['status']
    shippoTransaction.objectCreated=transaction['object_created']
    shippoTransaction.objectUpdated=transaction['object_updated']
    shippoTransaction.objectId=transaction['object_id']
    shippoTransaction.objectOwner=transaction['object_owner']
    shippoTransaction.rate=transaction['rate']
    shippoTransaction.trackingNumber=transaction['tracking_number']
    shippoTransaction.trackingStatus=transaction['tracking_status']
    shippoTransaction.trackingUrlProvider=transaction['tracking_url_provider']
    # cast from a boolean
    shippoTransaction.test=str(transaction['test'])
    shippoTransaction.shippoRateId=transaction['rate']
    shippoTransaction.save()
    serializer=ShippoTransactionSerializer(shippoTransaction)

    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'code': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(['post'])
@permission_classes([permissions.IsAuthenticated,IsOwner])
def generate_shippo_oauth_token(request):
    shippoRequest={}
    shippoRequest['client_id']=os.getenv('SHIPPO_CLIENT_ID')
    shippoRequest['client_secret']=os.getenv('SHIPPO_CLIENT_SECRET')
    shippoRequest['code']=request.data['code']
    shippoRequest['grant_type']='authorization_code'
    
    resp = requests.post('https://goshippo.com/oauth/access_token', data=shippoRequest)
    data=resp.json()
    shippoAccessToken=data['access_token']
    user=User.objects.get(email=request.user)
    user.shippoAccessToken=shippoAccessToken
    user.save()
    # can't do any additional data processing until I know what the response looks like
    return JsonResponse('Access token: '+str(shippoAccessToken),status=200,safe=False)

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'transactionId': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(['post'])
@permission_classes([permissions.IsAuthenticated,IsOwner])
def refund_shippo_transaction(request):
    import shippo
    user=User.objects.get(email=request.user)
    if user.userHasShippoAccount() and (os.getenv('ENVIRONMENT_TYPE')=='PRODUCTION'):
        shippo.config.api_key=user.shippoAccessToken
    else:
        shippo.config.api_key = os.getenv('SHIPPO_API_KEY')
    transactionId=request.data['transactionId']
    shippoTransaction = ShippoTransaction.objects.get(id=transactionId)
    shippoTransactionId = shippoTransaction.objectId
    refund = shippo.Refund.create(transaction=shippoTransactionId, asynchronous=False)
    shippoRefund = ShippoRefund.objects.create(owner=request.user, status=refund['status'], objectCreated=refund['object_created'], objectUpdated=refund['object_updated'], objectId=refund['object_id'], objectOwner=refund['object_owner'], test=refund['test'], transaction=shippoTransaction)
    serializer=ShippoRefundSerializer(shippoRefund)
    return Response(serializer.data)
