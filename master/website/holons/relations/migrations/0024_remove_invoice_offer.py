# Generated by Django 2.2 on 2021-05-23 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0023_auto_20210523_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='offer',
        ),
    ]
