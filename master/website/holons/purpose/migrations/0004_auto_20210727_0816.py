# Generated by Django 2.2 on 2021-07-27 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purpose', '0003_auto_20210727_0743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='context',
            old_name='user_handle_id',
            new_name='user_handle',
        ),
        migrations.RenameField(
            model_name='context',
            old_name='user_personal_id',
            new_name='user_personal',
        ),
    ]
