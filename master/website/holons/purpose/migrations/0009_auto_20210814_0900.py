# Generated by Django 2.2 on 2021-08-14 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purpose', '0008_keyresult_interval'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='keyresult',
            name='interval',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='purpose',
            name='start_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
