# Generated by Django 2.2 on 2021-08-04 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0009_auto_20210804_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='card_fingerprint',
            field=models.CharField(default='fail', max_length=255),
        ),
    ]
