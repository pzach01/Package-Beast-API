# Generated by Django 2.1.1 on 2021-08-12 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shipposervice', '0013_shippotransaction_trackingurlprovider'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippoRefund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objectState', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('status', models.CharField(blank=True, default='', max_length=16, null=True)),
                ('objectCreated', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('objectUpdated', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('objectId', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('objectOwner', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('test', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shippoRefund', to=settings.AUTH_USER_MODEL)),
                ('transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shippoRefund', to='shipposervice.ShippoTransaction')),
            ],
        ),
    ]
