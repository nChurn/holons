# Generated by Django 2.2 on 2021-02-17 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rays', '0045_auto_20210217_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directmessage',
            name='message_thread',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='rays.MessageThread'),
        ),
    ]