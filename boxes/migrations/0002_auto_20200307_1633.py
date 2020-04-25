# Generated by Django 2.1.1 on 2020-03-07 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='height',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='box',
            name='length',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='box',
            name='volume',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='box',
            name='width',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='box',
            name='xCenter',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='box',
            name='yCenter',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='box',
            name='zCenter',
            field=models.CharField(default='', max_length=100),
        ),
    ]
