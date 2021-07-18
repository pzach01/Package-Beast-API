from django.shortcuts import render


import os

from rest_framework import generics, viewsets, permissions
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from users.models import User
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi

from drf_yasg.utils import swagger_auto_schema


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'code': openapi.Schema(type=openapi.TYPE_STRING),
    }
))



@api_view(['post'])
@permission_classes([permissions.IsAuthenticated,IsOwner])
def generate_shippo_transaction(request):
    import shippo
    shippo.config.api_key = "shippo_test_41c916402deba95527751c894fd23fc03d7d8198"

    rateId=request.data['rateId']

    transaction = shippo.Transaction.create( 
        rate=rateId, 
        label_file_type="PDF", 
        asynchronous=False)

    return JsonResponse(transaction,status=200)

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