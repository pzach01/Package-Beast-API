# Generated by Django 2.1.1 on 2020-09-01 02:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0012_auto_20200901_0213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='stripeCustomerId',
            new_name='stripeId',
        ),
    ]