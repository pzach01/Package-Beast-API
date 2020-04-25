from django.shortcuts import render

# Create your views here.
from bins.models import Bin
from bins.serializers import BinListSerializer
from rest_framework import generics, viewsets, permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class BinList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get_queryset(self):
        user = self.request.user
        return Bin.objects.filter(owner=user)
    # queryset = Bin.objects.all()
    serializer_class = BinListSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class BinDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Bin.objects.all()
    serializer_class = BinListSerializer
