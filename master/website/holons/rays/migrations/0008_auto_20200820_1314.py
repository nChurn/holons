# Generated by Django 3.0.8 on 2020-08-20 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0007_auto_20200819_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='upworktalent',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='upworktalent',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
