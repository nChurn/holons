# Generated by Django 3.0.8 on 2020-09-07 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0017_auto_20200904_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(default=None, max_length=255, null=True)),
                ('city', models.CharField(default=None, max_length=255, null=True)),
                ('jobs_posted', models.IntegerField(default=None, null=True)),
                ('hire_rate', models.IntegerField(default=None, null=True)),
                ('open_jobs', models.IntegerField(default=None, null=True)),
                ('rating', models.IntegerField(default=None, null=True)),
                ('reviews_count', models.IntegerField(default=None, null=True)),
                ('guid', models.CharField(max_length=255)),
            ],
        ),
    ]
