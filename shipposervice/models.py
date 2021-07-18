from django.db import models
from django.contrib import admin
from quotes.models import Quote

# Create your models here.

class ShippoTransaction(models.Model):
    owner = models.ForeignKey(
        'users.User', related_name='shippo_transactions', on_delete=models.CASCADE)
    label_url = models.CharField(max_length=1012, default='', null=True, blank=True)
    quote = models.ForeignKey(Quote, related_name='shippo_transactions', on_delete=models.CASCADE)

    objectState=models.CharField(max_length=256,default='',null=True,blank=True)
    status=models.CharField(max_length=256,default='',null=True,blank=True)
    objectCreated=models.CharField(max_length=256,default='',null=True,blank=True)
    objectUpdated=models.CharField(max_length=256,default='',null=True,blank=True)
    objectId=models.CharField(max_length=256,default='',null=True,blank=True)
    objectOwner=models.CharField(max_length=256,default='',null=True,blank=True)
    # cast from a boolean
    wasTest=models.CharField(max_length=256,default='',null=True,blank=True)
    rateId=models.CharField(max_length=256,default='',null=True,blank=True)
admin.site.register(ShippoTransaction)