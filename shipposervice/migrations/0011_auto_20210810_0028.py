# Generated by Django 2.1.1 on 2021-08-10 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipposervice', '0010_auto_20210809_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippomessage',
            name='shippoTransaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='shipposervice.ShippoTransaction'),
        ),
    ]
