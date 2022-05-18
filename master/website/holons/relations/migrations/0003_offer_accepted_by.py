# Generated by Django 2.2 on 2021-02-10 17:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('relations', '0002_offer_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='accepted_by',
            field=models.ManyToManyField(blank=True, related_name='offers_accepted', to=settings.AUTH_USER_MODEL),
        ),
    ]
