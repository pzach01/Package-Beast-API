from django.db import models
from django.contrib import admin
from quotes.models import Quote

# Create your models here.

class ShippoTransaction(models.Model):
    owner = models.ForeignKey(
        'users.User', related_name='shippoTransaction', on_delete=models.CASCADE)
    label_url = models.CharField(max_length=1012, default='', null=True, blank=True)
    quote = models.OneToOneField(Quote, related_name='shippoTransaction', on_delete=models.CASCADE, blank=True, null=True)

    objectState=models.CharField(max_length=256,default='',null=True,blank=True)
    status=models.CharField(max_length=16,default='',null=True,blank=True)
    objectCreated=models.CharField(max_length=256,default='',null=True,blank=True)
    objectUpdated=models.CharField(max_length=256,default='',null=True,blank=True)
    objectId=models.CharField(max_length=256,default='',null=True,blank=True)
    objectOwner=models.CharField(max_length=256,default='',null=True,blank=True)
    rate=models.CharField(max_length=256,default='',null=True,blank=True)
    trackingNumber=models.CharField(max_length=256,default='',null=True,blank=True)
    trackingStatus=models.CharField(max_length=16,default='',null=True,blank=True)
    trackingUrlProvider=models.CharField(max_length=256,default='',null=True,blank=True)
    # cast from a boolean
    test=models.CharField(max_length=256,default='',null=True,blank=True)
    shippoRateId=models.CharField(max_length=256,default='',null=True,blank=True)

class ShippoMessage(models.Model):
    code = models.CharField(max_length=32,default='',null=True,blank=True)
    source = models.CharField(max_length=32,default='',null=True,blank=True)
    text = models.CharField(max_length=512,default='',null=True,blank=True)
    shippoTransaction = models.ForeignKey(ShippoTransaction, related_name='messages', on_delete=models.CASCADE, blank=True, null=True)

class ShippoRefund(models.Model):
    owner = models.ForeignKey(
        'users.User', related_name='shippoRefund', on_delete=models.CASCADE)
    status=models.CharField(max_length=16,default='',null=True,blank=True)
    objectCreated=models.CharField(max_length=256,default='',null=True,blank=True)
    objectUpdated=models.CharField(max_length=256,default='',null=True,blank=True)
    objectId=models.CharField(max_length=256,default='',null=True,blank=True)
    objectOwner=models.CharField(max_length=256,default='',null=True,blank=True)
    test=models.CharField(max_length=256,default='',null=True,blank=True)
    transaction=models.ForeignKey(ShippoTransaction, related_name='shippoRefund', on_delete=models.CASCADE, blank=True, null=True)

admin.site.register(ShippoTransaction)
admin.site.register(ShippoMessage)
admin.site.register(ShippoRefund)