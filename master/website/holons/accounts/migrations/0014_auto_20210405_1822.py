# Generated by Django 2.2 on 2021-04-05 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20210405_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userpic',
            field=models.ImageField(null=True, upload_to='userpics'),
        ),
    ]
