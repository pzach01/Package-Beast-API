from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from users.models import User
from users.serializers import UserSerializer

class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

