from django.shortcuts import render

# Create your views here.
from containers.models import Container
from containers.serializers import ContainerSerializer
from rest_framework import generics, viewsets, permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class ContainerList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Container.objects.filter(owner=user, arrangement__isnull=True)
    serializer_class = ContainerSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ContainerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
