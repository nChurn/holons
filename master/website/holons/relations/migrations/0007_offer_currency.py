# Generated by Django 2.2 on 2021-05-07 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0006_auto_20210507_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='currency',
            field=models.CharField(default='USD', max_length=3),
        ),
    ]
