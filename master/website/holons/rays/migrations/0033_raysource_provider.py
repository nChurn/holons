# Generated by Django 3.0.8 on 2020-10-15 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0032_auto_20201002_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='raysource',
            name='provider',
            field=models.TextField(default='upwork'),
        ),
    ]
