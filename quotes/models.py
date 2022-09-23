from django.db import models
from django.utils.timezone import now
from arrangements.models import Arrangement
from django.contrib import admin
from shipments.models import Shipment
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE


class Quote(SafeDeleteModel):
    safedelete_policy = SOFT_DELETE_CASCADE
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'users.User', related_name='quotes', on_delete=models.CASCADE)
    carrier = models.CharField(max_length=255,default='My carrier')
    cost=models.DecimalField(max_digits=7,decimal_places=2,default=-1)
    serviceDescription= models.CharField(max_length=255,default='SERVICE DESCRIPTION')
    daysToShip = models.CharField(max_length=255,blank=True, null=True, default="DAYS TO SHIP")
    scheduledDeliveryTime=models.CharField(max_length=255,blank=True,null=True,default='SCHEDULED DELIVERY TIME')
    shipment = models.ForeignKey(Shipment, related_name='quotes', on_delete=models.CASCADE, blank=True, null=True)
    arrangement = models.ForeignKey(Arrangement, related_name='quotes', on_delete=models.CASCADE, blank=True, null=True)
    shippoRateId=models.CharField(max_length=255,default='')

class ServiceLevel(models.Model):
    safedelete_policy = SOFT_DELETE_CASCADE
    name=models.CharField(max_length=32,blank=True,null=True,default='')
    token=models.CharField(max_length=32,blank=True,null=True,default='')
    terms=models.CharField(max_length=255,blank=True,null=True,default='')
    quote = models.OneToOneField(Quote, related_name='serviceLevel', on_delete=models.CASCADE, blank=True, null=True)

admin.site.register(ServiceLevel)
admin.site.register(Quote)