# Generated by Django 2.1.1 on 2020-06-18 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_units'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dateTimeFormat',
            field=models.CharField(default='MMM d, yyyy, h:mm aa', max_length=40),
        ),
    ]
