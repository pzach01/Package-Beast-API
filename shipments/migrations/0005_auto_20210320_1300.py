# Generated by Django 2.1.1 on 2021-03-20 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0004_auto_20210319_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='shipFromAddress',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipFromAddress', to='addresses.Address'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='shipToAddress',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipToAddress', to='addresses.Address'),
        ),
    ]