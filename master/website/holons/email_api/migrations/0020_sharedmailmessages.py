# Generated by Django 2.2 on 2021-01-09 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_mailbox', '0008_auto_20190219_1553'),
        ('email_api', '0019_delete_emailsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedMailMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_by_id', models.IntegerField(default=None)),
                ('mailbox_from_id', models.IntegerField(default=None)),
                ('mailbox_to_id', models.IntegerField(default=None)),
                ('messages', models.ManyToManyField(blank=True, to='django_mailbox.Message')),
            ],
        ),
    ]