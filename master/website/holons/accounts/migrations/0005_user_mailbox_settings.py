# Generated by Django 3.0.8 on 2020-08-28 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_api', '0008_emailsettings'),
        ('accounts', '0004_user_ray_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mailbox_settings',
            field=models.ManyToManyField(blank=True, related_name='users', to='email_api.EmailSettings'),
        ),
    ]
