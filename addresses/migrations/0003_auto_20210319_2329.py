# Generated by Django 2.1.1 on 2021-03-19 23:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20210319_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='fromOrTo',
        ),
        migrations.RemoveField(
            model_name='address',
            name='shipment',
        ),
    ]
