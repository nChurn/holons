# Generated by Django 2.2 on 2021-03-09 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210217_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cors_storage',
            field=models.TextField(default=''),
        ),
    ]
