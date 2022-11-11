from django.db import models
from django.contrib import admin
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

# Create your models here.

class Address(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'users.User', related_name='addresses', on_delete=models.CASCADE)
    name=models.CharField(max_length=100, blank=True, default='')
    phoneNumber=models.CharField(max_length=100, blank=True, default='')
    addressLine1 = models.CharField(max_length=100, blank=True, default='')
    addressLine2 = models.CharField(max_length=100, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    stateProvinceCode = models.CharField(max_length=50, blank=True, default='')
    postalCode = models.CharField(max_length=20, blank=True, default='')
    country=models.CharField(max_length=100,blank=True,default='')
admin.site.register(Address)


