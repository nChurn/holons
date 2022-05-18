# Generated by Django 2.2 on 2021-05-08 14:15

from django.db import migrations
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0008_offer_contract_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='id',
            field=hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='', primary_key=True, serialize=False),
        ),
    ]
