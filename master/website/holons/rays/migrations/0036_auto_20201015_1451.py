# Generated by Django 3.0.8 on 2020-10-15 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0035_auto_20201015_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upworktalent',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
