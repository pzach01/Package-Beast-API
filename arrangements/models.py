from django.db import models
from django.utils.timezone import now
import os
from arrangements.Box_Stuff_Python3_Only import box_stuff2 as bp
import json
from django.contrib import admin

class Arrangement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('users.User', related_name='arrangements', on_delete=models.CASCADE)
    bins = models.CharField(max_length=100, blank=True, default='')
    boxes = models.CharField(max_length=100, blank=True, default='')
    class Meta:
        ordering = ['created']

admin.site.register(Arrangement)

class BinLayout(models.Model):
    arrangement = models.ForeignKey(Arrangement, related_name='binLayout', on_delete=models.CASCADE)
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    length = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
    cost = models.FloatField(default=0.0)
    timedOut = models.BooleanField(default=False)


class BoxList(models.Model):
    binLayout = models.ForeignKey(BinLayout, related_name='boxList', on_delete=models.CASCADE)
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    length = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
    xCenter = models.FloatField(default=0.0)
    yCenter = models.FloatField(default=0.0)
    zCenter = models.FloatField(default=0.0)