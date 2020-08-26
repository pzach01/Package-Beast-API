# Generated by Django 2.1.1 on 2020-08-19 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('subscriptionType', models.CharField(max_length=20)),
                ('numRequestsLeft', models.IntegerField()),
                ('numItemsCanAdd', models.IntegerField()),
                ('numContainersCanAdd', models.IntegerField()),
                ('lastUpdateAbsoluteTime', models.FloatField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]