# Generated by Django 4.1.5 on 2023-01-16 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nippo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nippomodel',
            options={'verbose_name_plural': '日報'},
        ),
        migrations.AlterField(
            model_name='nippomodel',
            name='content',
            field=models.TextField(max_length=1000, verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='nippomodel',
            name='title',
            field=models.CharField(max_length=100, verbose_name='タイトル'),
        ),
    ]