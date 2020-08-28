# Generated by Django 2.1.1 on 2020-08-28 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0007_subscription_stripeid'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='stripeSubscriptionCurrentPeriodEnd',
            field=models.CharField(default=123456, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='stripeSubscriptionCustomer',
            field=models.CharField(default='12345', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='stripeSubscriptionId',
            field=models.CharField(default='12345', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='stripeSubscriptionItemDataPriceId',
            field=models.CharField(default='12345', max_length=50),
            preserve_default=False,
        ),
    ]