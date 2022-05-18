# Generated by Django 3.0.8 on 2020-08-30 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('email_api', '0010_mailbox_frontapp_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailImportStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=255)),
                ('conversation_count', models.IntegerField(default=0)),
                ('message_count', models.IntegerField(default=0)),
                ('mailbox', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='email_api.Mailbox')),
            ],
        ),
    ]