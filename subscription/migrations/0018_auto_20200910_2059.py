# Generated by Django 2.1.1 on 2020-09-10 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0017_auto_20200909_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripesubscription',
            name='createdStripe',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stripesubscription',
            name='current_period_end',
            field=models.IntegerField(default=0),
        ),
    ]
