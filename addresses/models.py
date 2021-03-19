from django.db import models
from django.contrib import admin
from shipments.models import Shipment

# Create your models here.

class Address(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'users.User', related_name='addresses', on_delete=models.CASCADE)
    addressLine1 = models.CharField(max_length=100, blank=True, default='')
    addressLine2 = models.CharField(max_length=100, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    stateProvince = models.CharField(max_length=50, blank=True, default='')
    country = models.CharField(max_length=50, blank=True, default='')
    postalCode = models.CharField(max_length=20, blank=True, default='')
    fromOrTo = models.CharField(max_length=4, blank=True, default='from')
    shipment = models.ForeignKey(Shipment, related_name='addresses', on_delete=models.CASCADE, blank=True, null=True)
admin.site.register(Address)