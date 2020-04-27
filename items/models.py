from django.db import models
from django.utils.timezone import now

# Create your models here.
class Item(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('users.User', related_name='boxes', on_delete=models.CASCADE)
    height = models.FloatField(default=0.0)
    width = models.FloatField(default=0.0)
    length = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)

    # def save(self, *args, **kwargs):
    #     self.volume = self.height * self.width * self.length
    #     super(Item, self).save(*args, **kwargs)