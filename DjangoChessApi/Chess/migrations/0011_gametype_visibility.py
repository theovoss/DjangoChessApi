# Generated by Django 3.1 on 2020-08-21 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chess', '0010_auto_20200817_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='gametype',
            name='visibility',
            field=models.CharField(
                choices=[
                    ('PR', 'PRIVATE'),
                    ('FR', 'FRIENDS'),
                    ('PU', 'PUBLIC'),
                    ('ST', 'STANDARD'),
                ],
                default='PR',
                max_length=2,
            ),
        ),
    ]
