# Generated by Django 2.1.1 on 2021-03-19 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0002_auto_20210318_0029'),
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='fromOrTo',
            field=models.CharField(blank=True, default='from', max_length=4),
        ),
        migrations.AddField(
            model_name='address',
            name='shipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='shipments.Shipment'),
        ),
    ]
