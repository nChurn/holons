# Generated by Django 2.2 on 2021-02-09 21:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(default='', max_length=255)),
                ('token_type', models.CharField(default='invitation', max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('valid_until', models.DateTimeField(default=None)),
                ('status', models.CharField(max_length=255)),
                ('issuer', models.ManyToManyField(blank=True, related_name='invitation_token', to=settings.AUTH_USER_MODEL)),
                ('used_by', models.ManyToManyField(blank=True, related_name='invitation_used', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
