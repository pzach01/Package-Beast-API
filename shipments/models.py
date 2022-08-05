from django.db import models
from django.utils.timezone import now
from django.contrib import admin
from addresses.models import Address
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

# Create your models here.


class Shipment(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'users.User', related_name='shipments', on_delete=models.CASCADE)
    title = models.CharField(max_length=255,default='My shipment')
    lastSelectedQuoteId = models.IntegerField(blank=True, null=True, default=0)
    multiBinPack = models.BooleanField(default=False)
    fitAllArrangementPossibleAPriori = models.BooleanField(default=False)
    arrangementFittingAllItemsFound=models.BooleanField(default=False)
    timeout = models.BooleanField(default=False)
    shipFromAddress = models.OneToOneField(Address, related_name='shipmentIsFromAddress', on_delete=models.CASCADE, blank=True, null=True)
    shipToAddress = models.OneToOneField(Address, related_name='shipmentIsToAddress', on_delete=models.CASCADE, blank=True, null=True)
    timingInformation=models.CharField(max_length=255,default='No timeout info')
    # false doesn't necessarily mean address was invalid, only that error thrown during shipment creation code (see serializer)
    validFromAddress=models.BooleanField(default=True)
    validToAddress=models.BooleanField(default=True)
    usedAllValidContainers=models.BooleanField(default=True)
    noErrorsMakingRequests=models.BooleanField(default=True)
    noValidRequests=models.BooleanField(default=False)
    calculationInProgress = models.BooleanField(default=False, null=True)
    dummyField = models.BooleanField(default=False, null=True)
admin.site.register(Shipment)