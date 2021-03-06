# Generated by Django 2.2 on 2021-07-31 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0006_subscription_stripe_subscription_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='last4',
            field=models.CharField(default=None, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='days_left',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
