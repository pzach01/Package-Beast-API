from django.shortcuts import render
import os
# Create your views here.
from shipments.models import Shipment
from shipments.serializers import ShipmentSerializer
from rest_framework import generics, permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class ShipmentList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Shipment.objects.prefetch_related('owner').prefetch_related('quotes', 'quotes__owner', 'quotes__arrangement', 'quotes__owner', 'quotes__arrangement', 'quotes__arrangement__containers', 'quotes__arrangement__items', 'quotes__arrangement__items__container').select_related('shipFromAddress').select_related('shipToAddress').filter(owner = user)
    serializer_class = ShipmentSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ShipmentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
