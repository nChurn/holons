# Generated by Django 3.0.8 on 2020-08-30 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_api', '0013_auto_20200830_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailbox',
            name='frontapp_token',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
