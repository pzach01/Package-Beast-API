# Generated by Django 2.1.1 on 2021-01-06 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_remove_item_dummyfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='dummyField2',
            field=models.CharField(default='howdy!', max_length=255),
        ),
    ]
