# Generated by Django 2.1.1 on 2020-08-30 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0009_auto_20200829_0402'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='stripeInvoiceIds',
            field=models.CharField(default='', max_length=250),
        ),
    ]