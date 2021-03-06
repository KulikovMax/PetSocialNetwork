# Generated by Django 3.2.9 on 2021-12-13 23:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20211214_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_request',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
