# Generated by Django 3.0.8 on 2020-10-28 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0038_auto_20201027_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='upworktalent',
            name='is_replied',
            field=models.BooleanField(default=False),
        ),
    ]
