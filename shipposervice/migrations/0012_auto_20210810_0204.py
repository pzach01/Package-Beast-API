# Generated by Django 2.1.1 on 2021-08-10 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipposervice', '0011_auto_20210810_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippotransaction',
            name='rate',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='shippotransaction',
            name='trackingNumber',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='shippotransaction',
            name='trackingStatus',
            field=models.CharField(blank=True, default='', max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='shippotransaction',
            name='status',
            field=models.CharField(blank=True, default='', max_length=16, null=True),
        ),
    ]