# Generated by Django 3.2.9 on 2022-08-29 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automate_process', '0005_auto_20220829_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracksourcedblastfetchtime',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
