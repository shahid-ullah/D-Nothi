# Generated by Django 3.2.9 on 2022-03-13 11:18

from django.db import migrations, models

import dashboard_generate.models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_generate', '0016_dashboardupdatelog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dashboardupdatelog',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='reportmobileappusersmodel',
            name='employee_record_ids',
            field=models.JSONField(
                default=dashboard_generate.models.EMPTY_DICTIONARY),
        ),
    ]
