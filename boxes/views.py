from django.shortcuts import render

# Create your views here.
from boxes.models import Box
from boxes.serializers import BoxListSerializer
from rest_framework import generics, viewsets, permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class BoxList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get_queryset(self):
        user = self.request.user
        return Box.objects.filter(owner=user)
    # queryset = Box.objects.all()
    serializer_class = BoxListSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class BoxDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Box.objects.all()
    serializer_class = BoxListSerializer
