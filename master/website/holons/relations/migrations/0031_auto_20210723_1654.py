# Generated by Django 2.2 on 2021-07-23 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0030_auto_20210704_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='offer',
            field=models.ManyToManyField(blank=True, related_name='invoices', to='relations.Offer'),
        ),
    ]
