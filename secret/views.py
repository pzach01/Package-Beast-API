from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
from rest_framework.decorators import api_view

@api_view()
def minimal(request):
    return Response({"message": "respond with MINIMAL plan client secret!"})

@api_view()
def standard(request):
    return Response({"message": "respond with STANDARD plan client secret!"})

@api_view()
def premium(request):
    return Response({"message": "respond with PREMIUM plan client secret!"})

@api_view()
def beast_mode(request):
    return Response({"message": "respond with BEAST MODE plan client secret!"})