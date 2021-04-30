from django.db import models
from django.utils.timezone import now
from arrangements.models import Arrangement
from django.contrib import admin
from shipments.models import Shipment

# Create your models here.


class Quote(models.Model):
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
admin.site.register(Quote)