# Generated by Django 3.2.7 on 2022-03-26 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0005_auto_20210429_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]
