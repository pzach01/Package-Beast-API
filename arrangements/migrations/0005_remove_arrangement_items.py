# Generated by Django 2.1.1 on 2020-05-23 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arrangements', '0004_remove_arrangement_containers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arrangement',
            name='items',
        ),
    ]
