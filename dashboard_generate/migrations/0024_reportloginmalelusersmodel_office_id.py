# Generated by Django 3.2.9 on 2022-09-19 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_generate', '0023_reportlogintotalusers_office_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportloginmalelusersmodel',
            name='office_id',
            field=models.PositiveIntegerField(db_index=True, default=0),
            preserve_default=False,
        ),
    ]
