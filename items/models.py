from django.db import models
from django.utils.timezone import now

# Create your models here.
class Item(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('users.User', related_name='boxes', on_delete=models.CASCADE)
    sku = models.CharField(max_length=255, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    length = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
    units = models.CharField(max_length=2, blank=False, default='in')
    cost = models.FloatField(default=0.0)