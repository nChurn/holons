# Generated by Django 2.2 on 2021-04-22 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0049_raycanned'),
        ('accounts', '0021_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rays_canned',
            field=models.ManyToManyField(blank=True, related_name='users', to='rays.RayCanned'),
        ),
    ]
