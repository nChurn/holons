# Generated by Django 2.2 on 2021-07-04 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0029_auto_20210628_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='offer',
            field=models.ManyToManyField(blank=True, related_name='invoices', to='relations.Offer'),
        ),
    ]
