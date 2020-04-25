from django.shortcuts import render

# Create your views here.
from arrangements.models import Arrangement
from arrangements.serializers import ArrangementSerializer, UserSerializer
from rest_framework import generics, viewsets, permissions

from arrangements.serializers import UserSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class ArrangementList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get_queryset(self):
        user = self.request.user
        return Arrangement.objects.filter(owner=user)
    

    queryset = Arrangement.objects.all()
    serializer_class = ArrangementSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class ArrangementDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Arrangement.objects.all()
    serializer_class = ArrangementSerializer
