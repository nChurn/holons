# Generated by Django 3.0.8 on 2020-10-15 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0034_upworktalent_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upworktalent',
            name='guid',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='upworktalent',
            name='link',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='upworktalent',
            name='title',
            field=models.CharField(max_length=1024),
        ),
    ]