# Generated by Django 2.2 on 2021-04-10 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20210405_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userpic',
            field=models.ImageField(null=True, upload_to='usg/soulspics'),
        ),
    ]
