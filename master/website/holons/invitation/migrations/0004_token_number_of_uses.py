# Generated by Django 2.2 on 2021-02-10 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0003_auto_20210210_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='number_of_uses',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
