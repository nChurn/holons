# Generated by Django 2.2 on 2021-02-08 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
    ]