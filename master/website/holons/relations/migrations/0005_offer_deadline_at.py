# Generated by Django 2.2 on 2021-05-07 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0004_offer_paragraphs'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='deadline_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
