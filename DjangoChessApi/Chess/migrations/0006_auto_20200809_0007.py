# Generated by Django 3.1 on 2020-08-09 04:07

import chess.chess_configurations
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chess', '0005_auto_20200807_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='data',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='game',
            name='history',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='gametype',
            name='rules',
            field=models.JSONField(default=chess.chess_configurations.get_standard_chess_pieces),
        ),
    ]