# scripts/reports/login_total_users.py
# SELECT count(DISTINCT(`employee_record_id`)) FROM `user_login_history` WHERE
# `created` >= '2022-01-01 00:00:00' AND `created` <= '2022-01-31 23:59:59'
from datetime import datetime, timedelta

import pandas as pd

from automate_process.models import UserLoginHistory
from backup_source_db.models import TrackBackupDBLastFetchTime
from dashboard_generate.models import ReportLoginTotalUsers

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

def format_and_load_to_mysql_db(request, *args, **kwargs):
    dataframe = kwargs['dataframe']
    grouped_report_date = dataframe.groupby(['report_date'], sort=False, as_index=False)

    batch_objects = []
    for report_date, frame in grouped_report_date:

        count_or_sum = int(frame['employee_record_id'].nunique())
        object_dict = generate_model_object_dict(request, report_date, count_or_sum, *args, **kwargs)

        employee_ids = {}

        for employee_id in frame.employee_record_id.values:
            employee_ids.setdefault(f'{employee_id}', 1)

        object_dict['employee_record_ids'] = employee_ids
        batch_objects.append(ReportLoginTotalUsers(**object_dict))

        if len(batch_objects) >= 100:
            ReportLoginTotalUsers.objects.bulk_create(batch_objects)
            batch_objects = []

    try:
        if batch_objects:
            ReportLoginTotalUsers.objects.bulk_create(batch_objects)
    except Exception as e:
        print(e)

    return None


def querysets_to_dataframe_and_refine(request=None, *args, **kwargs):
    querysets = kwargs.get('querysets')
    querysets_values = querysets.values('employee_record_id', 'created')
    dataframe = pd.DataFrame(querysets_values)

    # convert created object to datetime
    dataframe['created'] = pd.to_datetime(dataframe['created'], errors='coerce')
    dataframe = dataframe.loc[~dataframe['created'].isnull(), :]

    # generate date column
    dataframe['report_date'] = dataframe['created'].dt.date

    if not dataframe.empty:
        kwargs['dataframe'] = dataframe
        format_and_load_to_mysql_db(request, *args, **kwargs)


def generate_report(request=None, *args, **kwargs):
    print()
    print('start processing login_total_users report')

    querysets = utils.get_user_login_history_querysets(request, *args, **kwargs)
    querysets = querysets.exclude(created__isnull=True)

    if querysets.exists():
        kwargs['querysets'] = querysets
        querysets_to_dataframe_and_refine(request, *args, **kwargs)

    print('End processing login_total_users report')
    print()

    return None
