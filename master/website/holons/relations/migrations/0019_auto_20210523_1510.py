# Generated by Django 2.2 on 2021-05-23 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0018_auto_20210523_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='offer',
            field=models.ManyToManyField(blank=True, related_name='offer_invoices', to='relations.Offer'),
        ),
    ]
