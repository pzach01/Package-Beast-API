# Generated by Django 2.1.1 on 2020-09-01 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0013_auto_20200901_0243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='stripeId',
            new_name='stripeCustomerId',
        ),
    ]