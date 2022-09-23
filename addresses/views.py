from django.shortcuts import render

# Create your views here.
from addresses.models import Address
from addresses.serializers import AddressSerializer
from rest_framework import generics, viewsets, permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class AddressList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(owner=user)

    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer