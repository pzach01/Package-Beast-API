# Generated by Django 2.1.1 on 2020-09-03 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0015_auto_20200902_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripesubscription',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
