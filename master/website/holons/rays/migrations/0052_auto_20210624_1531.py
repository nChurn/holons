# Generated by Django 2.2 on 2021-06-24 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0051_auto_20210624_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raysource',
            name='stop_words',
            field=models.TextField(default='', null=True),
        ),
    ]
