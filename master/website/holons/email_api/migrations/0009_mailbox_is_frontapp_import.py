# Generated by Django 3.0.8 on 2020-08-28 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_api', '0008_emailsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailbox',
            name='is_frontapp_import',
            field=models.BooleanField(default=False),
        ),
    ]
