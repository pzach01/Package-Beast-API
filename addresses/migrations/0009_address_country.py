# Generated by Django 2.2 on 2022-11-11 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0008_remove_address_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]