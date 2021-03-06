# Generated by Django 3.0.8 on 2020-10-02 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0030_auto_20200927_2041'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomTalent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('link', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField()),
                ('guid', models.CharField(blank=True, max_length=255)),
                ('ray_source', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField()),
                ('is_archived', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_expired', models.BooleanField(default=False)),
            ],
        ),
    ]
