# Generated by Django 2.2 on 2021-01-09 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_api', '0020_sharedmailmessages'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharedmailmessages',
            name='assigned_to_id',
            field=models.IntegerField(default=None),
        ),
    ]