# Generated by Django 2.1.1 on 2021-08-10 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipposervice', '0012_auto_20210810_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippotransaction',
            name='trackingUrlProvider',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
    ]