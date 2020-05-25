# Generated by Django 2.1.1 on 2020-05-23 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arrangements', '0005_remove_arrangement_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrangement',
            name='containers',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='arrangement',
            name='items',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]