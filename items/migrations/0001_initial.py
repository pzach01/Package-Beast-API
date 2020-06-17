# Generated by Django 2.1.1 on 2020-06-17 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('arrangements', '0001_initial'),
        ('containers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sku', models.CharField(blank=True, default='', max_length=255)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('xDim', models.FloatField(default=0.0)),
                ('yDim', models.FloatField(default=0.0)),
                ('zDim', models.FloatField(default=0.0)),
                ('volume', models.FloatField(default=0.0)),
                ('units', models.CharField(default='in', max_length=2)),
                ('cost', models.FloatField(default=0.0)),
                ('xCenter', models.FloatField(blank=True, default=0.0, null=True)),
                ('yCenter', models.FloatField(blank=True, default=0.0, null=True)),
                ('zCenter', models.FloatField(blank=True, default=0.0, null=True)),
                ('arrangement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='arrangements.Arrangement')),
                ('container', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='containers.Container')),
            ],
        ),
    ]
