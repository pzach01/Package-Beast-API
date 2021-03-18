from django.db import models
from django.utils.timezone import now
from arrangements.models import Arrangement
from django.contrib import admin

# Create your models here.


class Quote(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'users.User', related_name='quotes', on_delete=models.CASCADE)
    carrier = models.CharField(max_length=255,default='My shipment')
    daysToShip = models.IntegerField(blank=True, null=True, default=0)
    arrangement = models.ForeignKey(Arrangement, related_name='quotes', on_delete=models.CASCADE, blank=True, null=True)
admin.site.register(Quote)