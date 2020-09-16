# Generated by Django 2.1.1 on 2020-09-09 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0016_stripesubscription_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='containersAllowed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subscription',
            name='containersUsed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subscription',
            name='itemsAllowed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subscription',
            name='itemsUsed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subscription',
            name='shipmentsAllowed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subscription',
            name='shipmentsUsed',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subscription',
            name='subscriptionType',
            field=models.CharField(default='none', max_length=20),
        ),
    ]