# Generated by Django 2.1.1 on 2020-08-29 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0008_auto_20200828_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='stripeSubscriptionId',
            field=models.CharField(default='null', max_length=50),
        ),
    ]
