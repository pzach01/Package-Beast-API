from django.db import models
from django.utils.timezone import now
from django.contrib import admin
from addresses.models import Address

# Create your models here.


class Shipment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'users.User', related_name='shipments', on_delete=models.CASCADE)
    title = models.CharField(max_length=255,default='My shipment')
    lastSelectedQuoteId = models.IntegerField(blank=True, null=True, default=0)
    multiBinPack = models.BooleanField(default=False)
    arrangementPossible = models.BooleanField(default=False)
    timeout = models.BooleanField(default=False)
    shipFromAddress = models.OneToOneField(Address, related_name='shipmentIsFromAddress', on_delete=models.CASCADE, blank=True, null=True)
    shipToAddress = models.OneToOneField(Address, related_name='shipmentIsToAddress', on_delete=models.CASCADE, blank=True, null=True)
    timingInformation=models.CharField(max_length=255,default='No timeout info')
admin.site.register(Shipment)