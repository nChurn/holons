# Generated by Django 3.0.8 on 2020-08-26 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_api', '0005_auto_20200826_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailmessagestatus',
            name='snoozed_until',
            field=models.DateTimeField(blank=True, default=None),
        ),
    ]
