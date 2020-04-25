# Generated by Django 2.1.1 on 2020-03-07 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boxes', '0002_auto_20200307_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='box',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='boxes', to=settings.AUTH_USER_MODEL),
        ),
    ]
