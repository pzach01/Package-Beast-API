# Generated by Django 2.1.1 on 2021-03-04 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_userstermsofservicerevision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='animationSpeed',
            field=models.IntegerField(default=100),
        ),
    ]
