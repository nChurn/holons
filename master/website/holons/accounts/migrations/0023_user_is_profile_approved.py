# Generated by Django 2.2 on 2021-04-24 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_user_rays_canned'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_profile_approved',
            field=models.BooleanField(default=False),
        ),
    ]