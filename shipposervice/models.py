from django.db import models
from django.contrib import admin
from quotes.models import Quote

# Create your models here.

class ShippoTransaction(models.Model):
    owner = models.ForeignKey(
        'users.User', related_name='shippo_transaction', on_delete=models.CASCADE)
    label_url = models.CharField(max_length=1012, default='', null=True, blank=True)
    quote = models.OneToOneField(Quote, related_name='shippo_transaction', on_delete=models.CASCADE, blank=True, null=True)

    objectState=models.CharField(max_length=256,default='',null=True,blank=True)
    status=models.CharField(max_length=256,default='',null=True,blank=True)
    objectCreated=models.CharField(max_length=256,default='',null=True,blank=True)
    objectUpdated=models.CharField(max_length=256,default='',null=True,blank=True)
    objectId=models.CharField(max_length=256,default='',null=True,blank=True)
    objectOwner=models.CharField(max_length=256,default='',null=True,blank=True)
    # cast from a boolean
    test=models.CharField(max_length=256,default='',null=True,blank=True)
    shippoRateId=models.CharField(max_length=256,default='',null=True,blank=True)
admin.site.register(ShippoTransaction)