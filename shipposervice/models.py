from django.db import models
from django.contrib import admin

# Create your models here.

class ShippoTransaction(models.Model):
    owner = models.ForeignKey(
        'users.User', related_name='shippo_transaction', on_delete=models.CASCADE)
    label_url = models.CharField(max_length=255, default='', null=True, blank=True)
admin.site.register(ShippoTransaction)