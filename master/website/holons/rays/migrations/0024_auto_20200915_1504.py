# Generated by Django 3.0.8 on 2020-09-15 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0023_auto_20200915_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raysource',
            name='budget_fixed',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='raysource',
            name='budget_rate',
            field=models.TextField(blank=True, default=''),
        ),
    ]
