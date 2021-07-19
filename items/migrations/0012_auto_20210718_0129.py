# Generated by Django 2.1.1 on 2021-07-18 01:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0011_remove_item_shipment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='weight',
            field=models.FloatField(default=1e-07, validators=[django.core.validators.MinValueValidator(1e-07)]),
        ),
    ]