# Generated by Django 3.2.9 on 2022-08-11 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backup_source_db', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackBackupDBLastFetchTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offices', models.DateTimeField()),
                ('users', models.DateTimeField()),
                ('employee_records', models.DateTimeField()),
                ('nisponno_records', models.DateTimeField()),
                ('user_login_history', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]