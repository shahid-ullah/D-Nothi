# Generated by Django 3.2.9 on 2022-09-13 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('automate_process', '0007_sourcedblog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sourcedblog',
            old_name='last_login_hisroty_time',
            new_name='last_login_history_time',
        ),
    ]