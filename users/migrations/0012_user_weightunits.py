# Generated by Django 2.1.1 on 2021-03-14 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210309_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='weightUnits',
            field=models.CharField(default='lb', max_length=2),
        ),
    ]
