# Generated by Django 3.2.9 on 2021-11-07 05:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import monthly_report.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monthly_report', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableNameModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CSVDataStorageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to=monthly_report.models.user_directory_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('table_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monthly_report.tablenamemodel')),
            ],
        ),
    ]
