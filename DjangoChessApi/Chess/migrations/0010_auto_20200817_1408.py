# Generated by Django 3.1 on 2020-08-17 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chess', '0009_auto_20200814_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='rule_description',
            field=models.TextField(default='unknown'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='rule_name',
            field=models.CharField(default='unknown', max_length=30),
            preserve_default=False,
        ),
    ]
