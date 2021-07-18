from django.db import models
from django.contrib import admin
from quotes.models import Quote

# Create your models here.

class ShippoTransaction(models.Model):
    owner = models.ForeignKey(
        'users.User', related_name='shippo_transactions', on_delete=models.CASCADE)
    label_url = models.CharField(max_length=255, default='', null=True, blank=True)
    quote = models.ForeignKey(Quote, related_name='shippo_transactions', on_delete=models.CASCADE)

admin.site.register(ShippoTransaction)