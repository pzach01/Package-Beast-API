from django.db import models
from django.utils.timezone import now
from arrangements.models import Arrangement
from django.contrib import admin

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
admin.site.register(Shipment)