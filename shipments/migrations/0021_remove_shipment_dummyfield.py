# Generated by Django 3.2.7 on 2022-08-04 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0020_auto_20220804_2316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipment',
            name='dummyField',
        ),
    ]
