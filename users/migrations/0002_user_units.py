# Generated by Django 2.1.1 on 2020-06-18 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='units',
            field=models.CharField(default='in', max_length=2),
        ),
    ]
