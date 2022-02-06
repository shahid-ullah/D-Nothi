# Generated by Django 3.2.9 on 2022-02-06 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard_generate', '0003_alter_reporttotalofficesmodel_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportNispottikrittoNothiModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_month_day', models.CharField(db_index=True, max_length=100)),
                ('year', models.PositiveIntegerField()),
                ('month', models.PositiveIntegerField()),
                ('day', models.PositiveIntegerField()),
                ('count_or_sum', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('report_date', models.CharField(max_length=100)),
                ('report_day', models.DateTimeField(blank=True, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'report_nispottikritto_nothi',
            },
        ),
    ]