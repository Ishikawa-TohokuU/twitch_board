# Generated by Django 4.1.5 on 2023-02-13 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_commentmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='stream_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='配信id'),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='streamer_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='ストリーマーid'),
        ),
    ]
