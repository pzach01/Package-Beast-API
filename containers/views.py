from django.shortcuts import render

# Create your views here.
from containers.models import Container, ThirdPartyContainer
from containers.serializers import ContainerSerializer, ThirdPartyContainerSerializer
from rest_framework import generics, permissions

ADMIN_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']

class IsAuthenticatedReadOrAdminWrite(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if (request.user and request.user.is_authenticated and request.method in permissions.SAFE_METHODS) or (request.user and request.user.is_authenticated and request.user.is_staff and request.method in ADMIN_METHODS):
            return True
        return False


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


class ThirdPartyContainerList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedReadOrAdminWrite]

    def get_queryset(self):
        return ThirdPartyContainer.objects.all()

    serializer_class = ThirdPartyContainerSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ThirdPartyContainerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedReadOrAdminWrite]
    queryset = ThirdPartyContainer.objects.all()
    serializer_class = ThirdPartyContainerSerializer
