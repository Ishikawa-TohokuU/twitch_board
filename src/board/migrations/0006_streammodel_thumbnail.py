# Generated by Django 4.1.5 on 2023-02-16 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_streamermodel_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='streammodel',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]