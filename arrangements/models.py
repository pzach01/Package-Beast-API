from django.db import models
from django.utils.timezone import now
import os
import json
from django.contrib import admin

class Arrangement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('users.User', related_name='arrangements', on_delete=models.CASCADE)
    containers = models.CharField(max_length=100, blank=True, default='')
    items = models.CharField(max_length=100, blank=True, default='')
    class Meta:
        ordering = ['created']

admin.site.register(Arrangement)

class ContainerLayout(models.Model):
    arrangement = models.ForeignKey(Arrangement, related_name='containerLayout', on_delete=models.CASCADE)
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    length = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
    cost = models.FloatField(default=0.0)
    timedOut = models.BooleanField(default=False)


class ItemList(models.Model):
    containerLayout = models.ForeignKey(ContainerLayout, related_name='itemList', on_delete=models.CASCADE)
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    length = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
    xCenter = models.FloatField(default=0.0)
    yCenter = models.FloatField(default=0.0)
    zCenter = models.FloatField(default=0.0)