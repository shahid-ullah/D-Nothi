# scripts/reports/login_total_users.py
# SELECT count(`employee_record_id`) FROM `user_login_history` WHERE
# `created` >= '2022-01-01 00:00:00' AND `created` <= '2022-01-31 23:59:59'
from datetime import datetime, timedelta

import pandas as pd
from automate_process.models import UserLoginHistory
from backup_source_db.models import BackupDBLog
from dashboard_generate.models import (
    ReportGenerationLog,
    ReportLoginTotalUsersNotDistinct,
)


def generate_model_object_dict(request, office_id, report_date, count_or_sum, *args, **kwargs):
    object_dic = {}
    object_dic['year'] = report_date.year
    object_dic['month'] = report_date.month
    object_dic['day'] = report_date.day
    object_dic['report_date'] = datetime(report_date.year, report_date.month, report_date.day)
    object_dic['counts'] = int(count_or_sum)
    object_dic['office_id'] = int(office_id)

    return object_dic


def format_and_load_to_mysql_db(request, *args, **kwargs):
    dataframe = kwargs['dataframe']
    grouped = dataframe.groupby(['office_id', 'report_date'], as_index=False, sort=False)['id'].size()

    batch_objects = []

    for office_id, report_date, counts in zip(
        grouped['office_id'].values, grouped['report_date'].values, grouped['size'].values
    ):

        object_dic = generate_model_object_dict(request, office_id, report_date, counts)
        batch_objects.append(ReportLoginTotalUsersNotDistinct(**object_dic))

        if len(batch_objects) >= 100:
            ReportLoginTotalUsersNotDistinct.objects.bulk_create(batch_objects)
            batch_objects = []

    if batch_objects:
        ReportLoginTotalUsersNotDistinct.objects.bulk_create(batch_objects)

    return None


def querysets_to_dataframe_and_refine(request=None, *args, **kwargs):
    querysets = kwargs.get('querysets')
    querysets_values = querysets.values('id', 'created', 'office_id')
    dataframe = pd.DataFrame(querysets_values)

    # convert created object to datetime
    dataframe['created'] = pd.to_datetime(dataframe['created'], errors='coerce')
    dataframe = dataframe.loc[~dataframe['created'].isnull(), :]
    dataframe = dataframe.loc[~dataframe['office_id'].isnull(), :]

    # generate date column
    dataframe['report_date'] = dataframe['created'].dt.date

    if not dataframe.empty:
        kwargs['dataframe'] = dataframe
        format_and_load_to_mysql_db(request, *args, **kwargs)


def get_user_login_history_querysets(*args, **kwargs):
    querysets = kwargs['querysets']

    if querysets is not None:
        return querysets

    querysets = UserLoginHistory.objects.using('source_db').all()

    if ReportLoginTotalUsersNotDistinct.objects.exists():
        last_fetch_time = ReportLoginTotalUsersNotDistinct.objects.last().report_date
        last_fetch_time = last_fetch_time + timedelta(days=1)
        querysets = querysets.filter(created__gte=last_fetch_time)

    return querysets


def generate_report(request=None, *args, **kwargs):
    print()
    print('start processing login_total_users not distinct report')

    querysets = get_user_login_history_querysets(request, *args, **kwargs)
    querysets = querysets.exclude(created__isnull=True)

    if querysets.exists():
        kwargs['querysets'] = querysets
        querysets_to_dataframe_and_refine(request, *args, **kwargs)

    print('End processing login_total_users not distinct report')
    print()

    return None
