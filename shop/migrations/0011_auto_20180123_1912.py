# Generated by Django 2.0 on 2018-01-23 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_game_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='url',
            field=models.URLField(max_length=300),
        ),
    ]