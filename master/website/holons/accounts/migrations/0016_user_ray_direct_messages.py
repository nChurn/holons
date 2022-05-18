# Generated by Django 2.2 on 2021-04-15 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0048_auto_20210218_1728'),
        ('accounts', '0015_auto_20210410_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ray_direct_messages',
            field=models.ManyToManyField(blank=True, related_name='users', to='rays.DirectMessage'),
        ),
    ]
