# Generated by Django 3.0.8 on 2020-08-26 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_api', '0004_mailmessagestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailmessagestatus',
            name='message_id',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
