from django.db import models
from django.utils.timezone import now


# Create your models here.
class Container(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('users.User', related_name='bins', on_delete=models.CASCADE)
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    length = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
    cost = models.FloatField(default=0.0)
    timedOut = models.BooleanField(default=False)