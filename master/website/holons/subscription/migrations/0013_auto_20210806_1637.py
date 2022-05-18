# Generated by Django 2.2 on 2021-08-06 16:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0012_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='days_left',
            field=models.IntegerField(default=0, null=True, verbose_name='Number of days left in subscription. Gets decreased daily by Django management command'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='expires_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='Last active day of the subscription'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Is subscription active'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='next_charge_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name="When the client's card will be charged again"),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='owner',
            field=models.ManyToManyField(blank=True, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='Who is using this subscription'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='stripe_customer_id',
            field=models.CharField(default='', max_length=255, verbose_name='Customer id inside Stripe'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='stripe_subscription_id',
            field=models.CharField(default='', max_length=255, verbose_name='Subscription id inside Stripe'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscription_type',
            field=models.CharField(default='holons core', max_length=255, verbose_name='String, identifiyng what is this subscription for (core service, plato etc...)'),
        ),
    ]
