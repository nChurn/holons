# Generated by Django 2.2 on 2021-07-27 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0032_auto_20210727_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='offer',
            field=models.ManyToManyField(blank=True, related_name='invoices', to='relations.Offer'),
        ),
    ]
