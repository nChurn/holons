# Generated by Django 2.2 on 2021-02-04 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moneta', '0001_initial'),
        ('timer', '0003_work_period_business_entity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work_period',
            name='business_entity',
        ),
        migrations.AddField(
            model_name='work_period',
            name='business_entity',
            field=models.ForeignKey(blank=True, default=False, on_delete=django.db.models.deletion.CASCADE, to='moneta.BusinessEntity'),
        ),
    ]