# Generated by Django 3.2.9 on 2022-09-27 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_generate', '0032_reportgenerationlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportlogintotalusersnotdistinct',
            name='ministry_id',
            field=models.PositiveIntegerField(default=0),
        ),
    ]