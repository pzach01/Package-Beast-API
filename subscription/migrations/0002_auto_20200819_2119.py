# Generated by Django 2.1.1 on 2020-08-19 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='lastUpdateAbsoluteTime',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='numContainersCanAdd',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='numItemsCanAdd',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='numRequestsLeft',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='subscriptionType',
        ),
    ]
