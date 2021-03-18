from django.shortcuts import render

# Create your views here.
from quotes.models import Quote
from quotes.serializers import QuoteSerializer
from rest_framework import generics, viewsets, permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class QuoteList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Quote.objects.filter(owner=user)

    serializer_class = QuoteSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuoteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
