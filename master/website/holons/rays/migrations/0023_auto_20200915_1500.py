# Generated by Django 3.0.8 on 2020-09-15 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0022_auto_20200912_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='raysource',
            name='budget_fixed',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='raysource',
            name='budget_rate',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='raysource',
            name='is_budget_empty_ok',
            field=models.BooleanField(default=True),
        ),
    ]