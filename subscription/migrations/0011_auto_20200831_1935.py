# Generated by Django 2.1.1 on 2020-08-31 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0010_subscription_stripeinvoiceids'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('stripeInvoiceId', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='stripeInvoiceIds',
        ),
        migrations.AddField(
            model_name='invoiceid',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.Subscription'),
        ),
    ]