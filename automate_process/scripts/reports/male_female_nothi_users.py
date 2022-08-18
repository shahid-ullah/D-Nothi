# scripts/reports/male_female_nothi_users.py
# SELECT COUNT(users.id) FROM users INNER JOIN employee_records on
# users.employee_record_id = employee_records.id WHERE date(users.created) <=
# '2020-09-31' and employee_records.gender = 2;

from datetime import datetime, timedelta

import pandas as pd

from automate_process.models import EmployeeRecords, Users
from backup_source_db.models import TrackBackupDBLastFetchTime
from dashboard_generate.models import (ReportFemaleNothiUsersModel,
                                       ReportMaleNothiUsersModel)

from . import utils


def generate_model_object_dict(request, report_date, count_or_sum, *args, **kwargs):
    object_dic = {}
    object_dic['year'] = report_date.year
    object_dic['month'] = report_date.month
    object_dic['day'] = report_date.day
    object_dic['year_month_day'] = str(report_date).replace('-', '')
    object_dic['report_date'] = str(report_date)
    object_dic['report_day'] = datetime(report_date.year, report_date.month, report_date.day)
    object_dic['count_or_sum'] = int(count_or_sum)

    return object_dic

def format_and_load_to_mysql_db(request=None, *args, **kwargs):
    dataframe = kwargs.get('dataframe')

    male_users_dataframe = dataframe.loc[dataframe['gender'] == '1', :]
    female_users_dataframe = dataframe.loc[dataframe['gender'] == '2', :]

    # groupby report_date
    male_grouped_report_date = male_users_dataframe.groupby(['report_date'], sort=False, as_index=False)['id'].size()
    female_grouped_report_date = female_users_dataframe.groupby(['report_date'], sort=False, as_index=False)['id'].size()

    batch_objects = []
    for report_date, male_count in zip(male_grouped_report_date['report_date'].values, male_grouped_report_date['size'].values):
        object_dict = generate_model_object_dict(request, report_date, male_count, *args, **kwargs)
        batch_objects.append(ReportMaleNothiUsersModel(**object_dict))

        if len(batch_objects) >= 100:
            ReportMaleNothiUsersModel.objects.bulk_create(batch_objects)
            batch_objects = []

    try:
        ReportMaleNothiUsersModel.objects.bulk_create(batch_objects)
    except Exception as e:
        pass

    batch_objects = []
    for report_date, female_count in zip(female_grouped_report_date['report_date'].values, female_grouped_report_date['size'].values):
        object_dict = generate_model_object_dict(request, report_date, female_count, *args, **kwargs)
        batch_objects.append(ReportFemaleNothiUsersModel(**object_dict))

        if len(batch_objects) >= 100:
            ReportFemaleNothiUsersModel.objects.bulk_create(batch_objects)
            batch_objects = []

    try:
        ReportFemaleNothiUsersModel.objects.bulk_create(batch_objects)
    except Exception as e:
        pass

    return None

def querysets_to_dataframe_and_refine(request=None, *args, **kwargs):
    users_querysets = kwargs['users_querysets']
    employee_querysets = kwargs['employee_querysets']

    users_querysets_values = users_querysets.values('created', 'employee_record_id')
    users_dataframe = pd.DataFrame(users_querysets_values)

    employee_querysets_values = employee_querysets.values('id', 'gender')
    employee_dataframe = pd.DataFrame(employee_querysets_values)

    users_dataframe = users_dataframe.loc[~users_dataframe.employee_record_id.isnull(), :]
    users_dataframe = users_dataframe.astype({'employee_record_id': int})

    employee_dataframe = employee_dataframe.loc[~employee_dataframe.id.isnull(), :]
    employee_dataframe = employee_dataframe.astype({'id': int})

    dataframe = pd.merge(
        users_dataframe,
        employee_dataframe,
        left_on=['employee_record_id'],
        right_on=['id'],
        suffixes=('_users', '_employee'),
    )
    dataframe = dataframe.astype({'gender': str})
    dataframe = dataframe.loc[~dataframe['created'].isnull(), :]
    dataframe['created'] = pd.to_datetime(dataframe.created, errors='coerce')
    dataframe = dataframe.loc[~dataframe.created.isnull(), :]

    # generate date column
    dataframe['report_date'] = dataframe['created'].dt.date

    if not dataframe.empty:
        kwargs['dataframe'] = dataframe
        format_and_load_to_mysql_db(request, *args, **kwargs)

    return None

def get_users_querysets(*args, **kwargs):
    last_fetch_time_object = TrackBackupDBLastFetchTime.objects.using('backup_source_db').last()
    querysets = Users.objects.using('source_db').all()
    try:
        last_fetch_time = last_fetch_time_object.users
        querysets = querysets.filter(created__gt=last_fetch_time)
    except AttributeError:
        last_fetch_time = ReportMaleNothiUsersModel.objects.last().report_day
        last_fetch_time = last_fetch_time + timedelta(days=1)
        querysets = querysets.filter(created__gte=last_fetch_time)

    return querysets

def generate_report(request=None, *args, **kwargs):
    print()
    print('start processing male & female nothi users report')

    users_querysets = get_users_querysets(*args, **kwargs)
    employee_querysets = utils.get_employee_records_querysets(*args, **kwargs)

    users_querysets = users_querysets.exclude(created__isnull=True)
    employee_querysets = employee_querysets.exclude(created__isnull=True)

    if users_querysets.exists() & employee_querysets.exists():
        kwargs['users_querysets'] = users_querysets
        kwargs['employee_querysets'] = employee_querysets
        querysets_to_dataframe_and_refine(request, *args, **kwargs)


    print('End processing male & female nothi users report')
    print()

    return None
