# Generated by Django 2.0 on 2018-01-23 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20180117_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='url',
            field=models.URLField(default='url', max_length=300),
        ),
    ]