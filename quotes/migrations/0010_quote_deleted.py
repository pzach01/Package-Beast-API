# Generated by Django 3.2.7 on 2022-03-26 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0009_servicelevel'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='deleted',
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]
