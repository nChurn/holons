# Generated by Django 3.0.8 on 2020-10-28 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0039_upworktalent_is_replied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upworktalent',
            name='templates',
            field=models.ManyToManyField(blank=True, default=False, related_name='tpl_messages', to='rays.RayTemplate'),
        ),
    ]
