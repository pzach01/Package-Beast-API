# Generated by Django 2.1.1 on 2021-04-23 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0008_auto_20210320_1308'),
        ('arrangements', '0002_arrangement_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrangement',
            name='shipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrangments', to='shipments.Shipment'),
        ),
    ]
