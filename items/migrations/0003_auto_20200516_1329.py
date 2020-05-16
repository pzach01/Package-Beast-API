# Generated by Django 2.1.1 on 2020-05-16 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_auto_20200516_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='cost',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='item',
            name='units',
            field=models.CharField(default='in', max_length=2),
        ),
    ]
