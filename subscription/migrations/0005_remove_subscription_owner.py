# Generated by Django 2.1.1 on 2020-08-19 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0004_subscription_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='owner',
        ),
    ]
