from django.shortcuts import render

# Create your views here.
from items.models import Item
from items.serializers import ItemSerializer
from rest_framework import generics, viewsets, permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class ItemList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Item.objects.filter(owner=user, arrangement__isnull=True, shipment__isnull=True)

    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
