# Generated by Django 2.2 on 2021-08-04 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0008_payment_payment_intent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlog',
            name='event_id',
            field=models.CharField(default='', max_length=255),
        ),
    ]
