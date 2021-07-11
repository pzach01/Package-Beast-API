from django.shortcuts import render
import os
# Create your views here.
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer
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
