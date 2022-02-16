# Table Name: login_history_employee_records (combined_table)
# report: login_male_female_nothi_users (combined)

from django.conf import settings

from ...models import EmployeeRecords, UserLoginHistory
from ..reports import login_male_female_users


def update(request=None, *args, **kwargs):
    user_login_history_objs, employee_records_objs = load_dataframe()

    login_history_employee_records_status = {}
    login_male_nothi_users_status = {}
    login_female_nothi_users_status = {}

    # login male & female nothi users
    try:
        (
            login_male_last_report_date,
            login_female_last_report_date,
        ) = login_male_female_users.update(
            request, user_login_history_objs, employee_records_objs, *args, **kwargs
        )
        login_male_nothi_users_status['last_report_date'] = str(
            login_male_last_report_date
        )
        login_male_nothi_users_status['status'] = 'success'

        login_female_nothi_users_status['last_report_date'] = str(
            login_female_last_report_date
        )
        login_female_nothi_users_status['status'] = 'success'

    except Exception as e:
        print(e)

    login_history_employee_records_status[
        'login_male_nothi_users'
    ] = login_male_nothi_users_status
    login_history_employee_records_status[
        'login_female_nothi_users'
    ] = login_female_nothi_users_status

    return login_history_employee_records_status


def load_dataframe():

    if settings.DEBUG:
        user_login_history_objs = UserLoginHistory.objects.using('source_db').all()[
            :1000
        ]
    else:
        user_login_history_objs = UserLoginHistory.objects.using('source_db').all()

    if settings.DEBUG:
        employee_records_objs = EmployeeRecords.objects.using('source_db').all()[:1000]
    else:
        employee_records_objs = EmployeeRecords.objects.using('source_db').all()

    return user_login_history_objs, employee_records_objs
