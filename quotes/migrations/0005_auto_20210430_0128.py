# Generated by Django 2.1.1 on 2021-04-30 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_quote_shipment'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=-1, max_digits=7),
        ),
        migrations.AddField(
            model_name='quote',
            name='scheduledDeliveryTime',
            field=models.CharField(default='SCHEDULED DELIVERY TIME', max_length=255),
        ),
        migrations.AddField(
            model_name='quote',
            name='serviceDescription',
            field=models.CharField(default='SERVICE DESCRIPTION', max_length=255),
        ),
        migrations.AlterField(
            model_name='quote',
            name='daysToShip',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
    ]
