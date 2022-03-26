from django.db import models
from django.utils.timezone import now
from django.contrib import admin
from shipments.models import Shipment
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

class Arrangement(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'users.User', related_name='arrangements', on_delete=models.CASCADE)
    multiBinPack = models.BooleanField(default=False)
    arrangementPossible = models.BooleanField(default=False)
    timeout = models.BooleanField(default=False)
    title=models.CharField(max_length=255,default='My shipment')
    shipment = models.ForeignKey(
        Shipment, related_name='arrangements', on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        ordering = ['created']

admin.site.register(Arrangement)
