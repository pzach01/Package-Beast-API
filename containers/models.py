from django.db import models
from django.utils.timezone import now
from arrangements.models import Arrangement
from django.contrib import admin
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

# Create your models here.
class Container(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'users.User', related_name='containers', on_delete=models.CASCADE)
    sku = models.CharField(max_length=255, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')
    xDim = models.FloatField(default=0.0)
    yDim = models.FloatField(default=0.0)
    zDim = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
    units = models.CharField(max_length=2, blank=False, default='in')
    cost = models.FloatField(default=0.0)
    arrangement = models.ForeignKey(
        Arrangement, related_name='containers', on_delete=models.CASCADE, blank=True, null=True)

admin.site.register(Container)