# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class EmployeeRecords(models.Model):
    name_eng = models.CharField(max_length=255)
    name_bng = models.CharField(max_length=255)
    father_name_eng = models.CharField(max_length=255, blank=True, null=True)
    father_name_bng = models.CharField(max_length=255, blank=True, null=True)
    mother_name_eng = models.CharField(max_length=255, blank=True, null=True)
    mother_name_bng = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    nid = models.CharField(max_length=32)
    nid_valid = models.IntegerField()
    bcn = models.CharField(max_length=32, blank=True, null=True)
    ppn = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=8, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    blood_group = models.CharField(max_length=4, blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    personal_email = models.CharField(max_length=255, blank=True, null=True)
    personal_mobile = models.CharField(max_length=255)
    alternative_mobile = models.CharField(max_length=255, blank=True, null=True)
    is_cadre = models.IntegerField()
    employee_grade = models.IntegerField(blank=True, null=True)
    employee_cadre_id = models.IntegerField(blank=True, null=True)
    employee_batch_id = models.IntegerField(blank=True, null=True)
    identity_no = models.CharField(max_length=64, blank=True, null=True)
    appointment_memo_no = models.CharField(max_length=50, blank=True, null=True)
    joining_date = models.DateTimeField(blank=True, null=True)
    service_rank_id = models.IntegerField(blank=True, null=True)
    service_grade_id = models.IntegerField(blank=True, null=True)
    service_ministry_id = models.IntegerField(blank=True, null=True)
    service_office_id = models.IntegerField(blank=True, null=True)
    current_office_ministry_id = models.IntegerField(blank=True, null=True)
    current_office_layer_id = models.IntegerField(blank=True, null=True)
    current_office_id = models.IntegerField(blank=True, null=True)
    current_office_unit_id = models.IntegerField(blank=True, null=True)
    current_office_joining_date = models.DateTimeField(blank=True, null=True)
    current_office_designation_id = models.IntegerField(blank=True, null=True)
    current_office_address = models.CharField(max_length=255, blank=True, null=True)
    e_sign = models.CharField(max_length=255, blank=True, null=True)
    d_sign = models.CharField(max_length=255, blank=True, null=True)
    image_file_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    default_sign = models.IntegerField()
    hard_signature = models.IntegerField()
    soft_signature = models.IntegerField()
    cert_id = models.CharField(max_length=50, blank=True, null=True)
    cert_type = models.CharField(max_length=10, blank=True, null=True)
    cert_provider = models.CharField(max_length=20, blank=True, null=True)
    cert_serial = models.CharField(max_length=250, blank=True, null=True)
    created_by = models.IntegerField()
    modified_by = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_records'


class Offices(models.Model):
    office_ministry_id = models.IntegerField()
    office_layer_id = models.IntegerField()
    custom_layer_id = models.IntegerField(blank=True, null=True)
    office_origin_id = models.IntegerField()
    office_name_eng = models.CharField(max_length=255)
    office_name_bng = models.CharField(max_length=255)
    geo_division_id = models.IntegerField()
    geo_district_id = models.IntegerField()
    geo_upazila_id = models.IntegerField()
    geo_union_id = models.IntegerField()
    office_address = models.CharField(max_length=255, blank=True, null=True)
    digital_nothi_code = models.CharField(max_length=32, blank=True, null=True)
    reference_code = models.CharField(max_length=32, blank=True, null=True)
    office_code = models.CharField(max_length=32, blank=True, null=True)
    office_phone = models.CharField(max_length=255, blank=True, null=True)
    office_mobile = models.CharField(max_length=255, blank=True, null=True)
    office_fax = models.CharField(max_length=255, blank=True, null=True)
    office_email = models.CharField(max_length=255, blank=True, null=True)
    office_web = models.CharField(max_length=255, blank=True, null=True)
    parent_office_id = models.IntegerField()
    active_status = models.IntegerField()
    unit_organogram_edit_option = models.IntegerField(blank=True, null=True)
    unit_organogram_edit_option_status_updated_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField()
    modified_by = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'offices'


class UserLoginHistory(models.Model):
    is_mobile = models.IntegerField()
    client_ip = models.CharField(max_length=30)
    device_name = models.CharField(max_length=255)
    browser_name = models.CharField(max_length=255)
    employee_record_id = models.BigIntegerField()
    ministry_id = models.IntegerField()
    layer_id = models.IntegerField()
    origin_id = models.IntegerField()
    office_id = models.IntegerField()
    office_unit_id = models.BigIntegerField()
    office_unit_organogram = models.BigIntegerField()
    office_name = models.CharField(max_length=200, blank=True, null=True)
    unit_name = models.CharField(max_length=200)
    organogram_name = models.CharField(max_length=200)
    user_id = models.IntegerField(blank=True, null=True)
    employee_name = models.CharField(max_length=250, blank=True, null=True)
    mobile_number = models.CharField(max_length=13, blank=True, null=True)
    employee_email = models.CharField(max_length=100, blank=True, null=True)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(blank=True, null=True)
    network_information = models.TextField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    device_type = models.CharField(max_length=50)
    device_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_login_history'


class Users(models.Model):
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    user_alias = models.CharField(max_length=50)
    hash_change_password = models.CharField(max_length=255, blank=True, null=True)
    user_role_id = models.IntegerField()
    is_admin = models.IntegerField()
    active = models.IntegerField(blank=True, null=True)
    user_status = models.CharField(max_length=255, db_collation='latin1_swedish_ci')
    is_email_verified = models.IntegerField(blank=True, null=True)
    email_verify_code = models.CharField(max_length=255, db_collation='latin1_swedish_ci', blank=True, null=True)
    verification_date = models.DateField(blank=True, null=True)
    ssn = models.CharField(max_length=255, db_collation='latin1_swedish_ci', blank=True, null=True)
    force_password_change = models.IntegerField(blank=True, null=True)
    last_password_change = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    modified_by = models.CharField(max_length=100)
    photo = models.CharField(max_length=255, blank=True, null=True)
    employee_record_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
