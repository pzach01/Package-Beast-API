from django.db import models
from django.utils.timezone import now
from django.contrib import admin


class Arrangement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'users.User', related_name='arrangements', on_delete=models.CASCADE)
    multiBinPack = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']


admin.site.register(Arrangement)
