# Generated by Django 3.2.9 on 2022-08-09 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackupEmployeeRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=255)),
                ('name_bng', models.CharField(max_length=255)),
                ('father_name_eng', models.CharField(blank=True, max_length=255, null=True)),
                ('father_name_bng', models.CharField(blank=True, max_length=255, null=True)),
                ('mother_name_eng', models.CharField(blank=True, max_length=255, null=True)),
                ('mother_name_bng', models.CharField(blank=True, max_length=255, null=True)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
                ('nid', models.CharField(max_length=32)),
                ('nid_valid', models.IntegerField()),
                ('bcn', models.CharField(blank=True, max_length=32, null=True)),
                ('ppn', models.CharField(blank=True, max_length=32, null=True)),
                ('gender', models.CharField(blank=True, max_length=8, null=True)),
                ('religion', models.CharField(blank=True, max_length=50, null=True)),
                ('blood_group', models.CharField(blank=True, max_length=4, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=20, null=True)),
                ('personal_email', models.CharField(blank=True, max_length=255, null=True)),
                ('personal_mobile', models.CharField(max_length=255)),
                ('alternative_mobile', models.CharField(blank=True, max_length=255, null=True)),
                ('is_cadre', models.IntegerField()),
                ('employee_grade', models.IntegerField(blank=True, null=True)),
                ('employee_cadre_id', models.IntegerField(blank=True, null=True)),
                ('employee_batch_id', models.IntegerField(blank=True, null=True)),
                ('identity_no', models.CharField(blank=True, max_length=64, null=True)),
                ('appointment_memo_no', models.CharField(blank=True, max_length=50, null=True)),
                ('joining_date', models.DateTimeField(blank=True, null=True)),
                ('service_rank_id', models.IntegerField(blank=True, null=True)),
                ('service_grade_id', models.IntegerField(blank=True, null=True)),
                ('service_ministry_id', models.IntegerField(blank=True, null=True)),
                ('service_office_id', models.IntegerField(blank=True, null=True)),
                ('current_office_ministry_id', models.IntegerField(blank=True, null=True)),
                ('current_office_layer_id', models.IntegerField(blank=True, null=True)),
                ('current_office_id', models.IntegerField(blank=True, null=True)),
                ('current_office_unit_id', models.IntegerField(blank=True, null=True)),
                ('current_office_joining_date', models.DateTimeField(blank=True, null=True)),
                ('current_office_designation_id', models.IntegerField(blank=True, null=True)),
                ('current_office_address', models.CharField(blank=True, max_length=255, null=True)),
                ('e_sign', models.CharField(blank=True, max_length=255, null=True)),
                ('d_sign', models.CharField(blank=True, max_length=255, null=True)),
                ('image_file_name', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.IntegerField()),
                ('default_sign', models.IntegerField()),
                ('hard_signature', models.IntegerField()),
                ('soft_signature', models.IntegerField()),
                ('cert_id', models.CharField(blank=True, max_length=50, null=True)),
                ('cert_type', models.CharField(blank=True, max_length=10, null=True)),
                ('cert_provider', models.CharField(blank=True, max_length=20, null=True)),
                ('cert_serial', models.CharField(blank=True, max_length=250, null=True)),
                ('created_by', models.IntegerField()),
                ('modified_by', models.IntegerField()),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'backup_employee_records',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BackupNisponnoRecords',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nothi_master_id', models.IntegerField()),
                ('nothi_part_no', models.IntegerField()),
                ('type', models.CharField(max_length=100)),
                ('nothi_onucched_id', models.IntegerField(blank=True, null=True)),
                ('potrojari_id', models.IntegerField()),
                ('nothi_office_id', models.IntegerField()),
                ('office_id', models.IntegerField()),
                ('unit_id', models.IntegerField()),
                ('designation_id', models.IntegerField()),
                ('employee_id', models.IntegerField()),
                ('upokarvogi', models.IntegerField()),
                ('potrojari_internal_own', models.IntegerField()),
                ('potrojari_internal_other', models.IntegerField()),
                ('dak_srijito', models.IntegerField()),
                ('operation_date', models.DateTimeField()),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
            ],
            options={
                'db_table': 'backup_nisponno_records',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BackupOffices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office_ministry_id', models.IntegerField()),
                ('office_layer_id', models.IntegerField()),
                ('custom_layer_id', models.IntegerField(blank=True, null=True)),
                ('office_origin_id', models.IntegerField()),
                ('office_name_eng', models.CharField(max_length=255)),
                ('office_name_bng', models.CharField(max_length=255)),
                ('geo_division_id', models.IntegerField()),
                ('geo_district_id', models.IntegerField()),
                ('geo_upazila_id', models.IntegerField()),
                ('geo_union_id', models.IntegerField()),
                ('office_address', models.CharField(blank=True, max_length=255, null=True)),
                ('digital_nothi_code', models.CharField(blank=True, max_length=32, null=True)),
                ('reference_code', models.CharField(blank=True, max_length=32, null=True)),
                ('office_code', models.CharField(blank=True, max_length=32, null=True)),
                ('office_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('office_mobile', models.CharField(blank=True, max_length=255, null=True)),
                ('office_fax', models.CharField(blank=True, max_length=255, null=True)),
                ('office_email', models.CharField(blank=True, max_length=255, null=True)),
                ('office_web', models.CharField(blank=True, max_length=255, null=True)),
                ('parent_office_id', models.IntegerField()),
                ('active_status', models.IntegerField()),
                ('unit_organogram_edit_option', models.IntegerField(blank=True, null=True)),
                ('unit_organogram_edit_option_status_updated_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField()),
                ('modified_by', models.IntegerField()),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'backup_offices',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BackupUserLoginHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_mobile', models.IntegerField()),
                ('client_ip', models.CharField(max_length=30)),
                ('device_name', models.CharField(max_length=255)),
                ('browser_name', models.CharField(max_length=255)),
                ('employee_record_id', models.BigIntegerField()),
                ('ministry_id', models.IntegerField()),
                ('layer_id', models.IntegerField()),
                ('origin_id', models.IntegerField()),
                ('office_id', models.IntegerField()),
                ('office_unit_id', models.BigIntegerField()),
                ('office_unit_organogram', models.BigIntegerField()),
                ('office_name', models.CharField(blank=True, max_length=200, null=True)),
                ('unit_name', models.CharField(max_length=200)),
                ('organogram_name', models.CharField(max_length=200)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('employee_name', models.CharField(blank=True, max_length=250, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=13, null=True)),
                ('employee_email', models.CharField(blank=True, max_length=100, null=True)),
                ('login_time', models.DateTimeField()),
                ('logout_time', models.DateTimeField(blank=True, null=True)),
                ('network_information', models.TextField()),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('modified_by', models.IntegerField(blank=True, null=True)),
                ('token', models.TextField(blank=True, null=True)),
                ('device_type', models.CharField(max_length=50)),
                ('device_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'backup_user_login_history',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='BackupUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('user_alias', models.CharField(max_length=50)),
                ('hash_change_password', models.CharField(blank=True, max_length=255, null=True)),
                ('user_role_id', models.IntegerField()),
                ('is_admin', models.IntegerField()),
                ('active', models.IntegerField(blank=True, null=True)),
                ('user_status', models.CharField(db_collation='latin1_swedish_ci', max_length=255)),
                ('is_email_verified', models.IntegerField(blank=True, null=True)),
                ('email_verify_code', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=255, null=True)),
                ('verification_date', models.DateField(blank=True, null=True)),
                ('ssn', models.CharField(blank=True, db_collation='latin1_swedish_ci', max_length=255, null=True)),
                ('force_password_change', models.IntegerField(blank=True, null=True)),
                ('last_password_change', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_by', models.CharField(max_length=100)),
                ('photo', models.CharField(blank=True, max_length=255, null=True)),
                ('employee_record_id', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'backup_users',
                'managed': True,
            },
        ),
    ]