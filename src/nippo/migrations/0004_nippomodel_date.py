# Generated by Django 4.1.5 on 2023-01-19 13:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('nippo', '0003_nippomodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='nippomodel',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
