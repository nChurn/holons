# Generated by Django 2.2 on 2021-04-14 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moneta', '0001_initial'),
        ('timer', '0005_work_period_comment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='work_period',
            new_name='WorkPeriod',
        ),
    ]
