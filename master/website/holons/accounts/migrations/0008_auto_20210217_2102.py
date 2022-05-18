# Generated by Django 2.2 on 2021-02-17 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0043_ray'),
        ('accounts', '0007_auto_20210217_2021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='rays_direct_treads',
        ),
        migrations.AddField(
            model_name='user',
            name='rays_direct',
            field=models.ManyToManyField(blank=True, related_name='users', to='rays.Ray'),
        ),
    ]
