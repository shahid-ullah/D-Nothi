# Table Name: users_employee_records (combined_table)
# Report1: male_nothi_users
# Report2: female_nothi_users
import json
import os

from django.conf import settings

from ...models import EmployeeRecords, Users
from ..reports import male_nothi_users


def update():
    users_objs, employee_records_objs = load_dataframe()
    # breakpoint()

    users_employee_records = {}
    status = {}

    # update male & female nothi users
    try:
        male_year_report, female_year_report = male_nothi_users.update(
            users_objs, employee_records_objs
        )
        users_employee_records['male_nothi_users'] = male_year_report
        users_employee_records['female_nothi_users'] = female_year_report
        status['male_female_nothi_users'] = 'success'
    except Exception as e:
        users_employee_records['male_nothi_users'] = []
        users_employee_records['female_nothi_users'] = []
        status['male_female_nothi_users'] = 'Failed'
        print(e)

    dir_name = 'temporary_data'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    path = dir_name + "/" + "users_employee_records.json"

    print(f"Saving graph data ...{path}")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(users_employee_records, f, ensure_ascii=False, indent=4)
    return users_employee_records, status


def load_dataframe():
    # if settings.DEBUG:
    #     users_objs = Users.objects.using('source_db').all()[:100000]
    #     employee_records_objs = EmployeeRecords.objects.using('source_db').all()[
    #         :100000
    #     ]
    # else:
    users_objs = Users.objects.using('source_db').all()
    employee_records_objs = EmployeeRecords.objects.using('source_db').all()
    # breakpoint()

    return users_objs, employee_records_objs
