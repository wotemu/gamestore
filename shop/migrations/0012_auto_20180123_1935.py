# Generated by Django 2.0 on 2018-01-23 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20180123_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='url',
            field=models.URLField(max_length=300, unique=True),
        ),
    ]
