# Generated by Django 2.1.1 on 2020-12-14 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0024_remove_subscription_containersused'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='containersAllowed',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='itemsAllowed',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='shipmentsAllowed',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscriptionType',
            field=models.CharField(default='trial', max_length=20),
        ),
    ]
