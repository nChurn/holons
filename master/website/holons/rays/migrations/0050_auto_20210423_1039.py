# Generated by Django 2.2 on 2021-04-23 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0049_raycanned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raycanned',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
    ]
