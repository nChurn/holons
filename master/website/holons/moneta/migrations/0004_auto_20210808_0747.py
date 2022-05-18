# Generated by Django 2.2 on 2021-08-08 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purpose', '0006_auto_20210804_1634'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moneta', '0003_auto_20210805_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('context', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='costs_tags', to='purpose.Context')),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='costs_tags', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='fixedcost',
            old_name='value',
            new_name='amount',
        ),
        migrations.RenameField(
            model_name='fixedcost',
            old_name='deleted_at',
            new_name='finished_at',
        ),
        migrations.AddField(
            model_name='fixedcost',
            name='context',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fixed_costs', to='purpose.Context'),
        ),
        migrations.AlterField(
            model_name='fixedcost',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='fixed_costs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='fixedcost',
            name='started_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='paysendaccount',
            name='card_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='VariableCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('context', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variable_costs', to='purpose.Context')),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='variable_costs', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(related_name='variable_costs', to='moneta.CostTag')),
            ],
        ),
        migrations.AddField(
            model_name='fixedcost',
            name='tags',
            field=models.ManyToManyField(related_name='fixed_costs', to='moneta.CostTag'),
        ),
    ]