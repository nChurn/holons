# Generated by Django 2.2 on 2021-05-30 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0005_auto_20210530_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='stripe_subscription_id',
            field=models.CharField(default='', max_length=255),
        ),
    ]
