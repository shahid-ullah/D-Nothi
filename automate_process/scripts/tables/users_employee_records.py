# Table Name: users_employee_records (combined_table)
# Report1: male_nothi_users
# Report2: female_nothi_users

from django.conf import settings

from ...models import EmployeeRecords, Users
from ..reports import male_female_nothi_users


def update(request=None, *args, **kwargs):
    users_objs, employee_records_objs = load_dataframe()

    users_employee_records_status = {}
    male_nothi_users_status = {}
    female_nothi_users_status = {}

    # male & female nothi users
    try:
        male_last_report_date, female_last_report_date = male_female_nothi_users.update(
            request, users_objs, employee_records_objs, *args, **kwargs
        )
        male_nothi_users_status['last_report_date'] = str(male_last_report_date)
        male_nothi_users_status['status'] = 'success'

        female_nothi_users_status['last_report_date'] = str(female_last_report_date)
        female_nothi_users_status['status'] = 'success'

    except Exception as e:
        print(e)

    users_employee_records_status['male_nothi_users'] = male_nothi_users_status
    users_employee_records_status['female_nothi_users'] = female_nothi_users_status

    return users_employee_records_status


def load_dataframe():

    if settings.DEBUG:
        users_objs = Users.objects.using('source_db').all()[:1000]
    else:
        users_objs = Users.objects.using('source_db').all()

    if settings.DEBUG:
        employee_records_objs = EmployeeRecords.objects.using('source_db').all()[:1000]
    else:
        employee_records_objs = EmployeeRecords.objects.using('source_db').all()

    return users_objs, employee_records_objs
