# Generated by Django 2.2 on 2021-06-28 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0028_auto_20210624_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='offer',
            field=models.ManyToManyField(blank=True, related_name='invoices', to='relations.Offer'),
        ),
    ]
