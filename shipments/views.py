from django.shortcuts import render
import os
# Create your views here.
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer
from rest_framework import generics, viewsets, permissions
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

@api_view(['post'])
@permission_classes([permissions.IsAuthenticated])
def generate_shippo_oauth_token(request):
    shippoRequest={}
    shippoRequest['client_id']=os.getenv('SHIPPO_CLIENT_ID')
    shippoRequest['client_secret']=os.getenv('SHIPPO_CLIENT_SECRET')
    shippoRequest['code']=request.data['code']
    shippoRequest['grant_type']='authorization_code'
    resp = requests.post('https://goshippo.com/oauth/access_token', data=shippoRequest)
    # can't do any additional data processing until I know what the response looks like
    return JsonResponse(resp.json())

class ShipmentList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Shipment.objects.filter(owner=user)

    serializer_class = ShipmentSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ShipmentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
