from django.db import models
from django.utils.timezone import now
from containers.models import Container
from arrangements.models import Arrangement
from shipments.models import Shipment
from django.contrib import admin
from django.core.validators import MinValueValidator
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
# Create your models here.


class Item(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'users.User', related_name='items', on_delete=models.CASCADE)
    sku = models.CharField(max_length=255, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')
    length = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    height = models.FloatField(default=0.0)
    xDim = models.FloatField(default=0.0)
    yDim = models.FloatField(default=0.0)
    zDim = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
    units = models.CharField(max_length=2, blank=False, default='in')
    cost = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0000001,validators=[MinValueValidator(.0000001)])
    weightUnits = models.CharField(max_length=2, blank=False, default='lb')
    # We could do it like this but we just need a reference to the item id
    # This reduces db calls in arrangements serializer
    # masterItem = models.ForeignKey('items.Item', related_name="items", on_delete=models.CASCADE, blank=True, null=True)
    masterItemId = models.IntegerField(blank=True, null=True, default=0)
    container = models.ForeignKey(
        Container, related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    arrangement = models.ForeignKey(
        Arrangement, related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    xCenter = models.FloatField(default=0.0, blank=True, null=True)
    yCenter = models.FloatField(default=0.0, blank=True, null=True)
    zCenter = models.FloatField(default=0.0, blank=True, null=True)

admin.site.register(Item)
