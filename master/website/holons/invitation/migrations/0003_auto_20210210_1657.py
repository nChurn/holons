# Generated by Django 2.2 on 2021-02-10 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0002_auto_20210210_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='valid_until',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
