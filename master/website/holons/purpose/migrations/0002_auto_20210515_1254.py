# Generated by Django 2.2 on 2021-05-15 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moneta', '0001_initial'),
        ('purpose', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('is_draft', models.BooleanField(default=False)),
                ('start_at', models.DateTimeField(auto_now=True)),
                ('finish_at', models.DateTimeField(blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('is_personal', models.BooleanField(default=False)),
                ('is_handle', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('entities', models.ManyToManyField(blank=True, related_name='purpose_contexts', to='moneta.BusinessEntity')),
                ('seasons', models.ManyToManyField(blank=True, related_name='contexts', to='purpose.Season')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='context',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='purpose.Context'),
        ),
    ]
