# Generated by Django 3.2.9 on 2021-11-07 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monthly_report', '0002_csvdatastoragemodel_tablenamemodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='csvdatastoragemodel',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='tablenamemodel',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='tablenamemodel',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
