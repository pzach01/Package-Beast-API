# Generated by Django 3.2.7 on 2022-08-04 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0021_remove_shipment_dummyfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='dummyField3',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
