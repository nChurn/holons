# Generated by Django 3.0.8 on 2020-10-02 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0031_customtalent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customtalent',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
