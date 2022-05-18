# Generated by Django 2.2 on 2020-12-16 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(null=True)),
                ('worked_hours', models.IntegerField(null=True)),
                ('paid_hours', models.IntegerField(null=True)),
                ('rate', models.FloatField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='user',
        ),
        migrations.AlterField(
            model_name='work_period',
            name='duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='work_period',
            name='timer_start',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='work_period',
            name='timer_stop',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='work_period',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
    ]
