# Generated by Django 3.0.8 on 2020-09-08 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0018_clientstats'),
    ]

    operations = [
        migrations.AddField(
            model_name='raysource',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
