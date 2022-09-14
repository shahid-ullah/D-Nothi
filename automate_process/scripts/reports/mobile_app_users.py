# automate_process/scripts/reports/mobile_app_users.py
# SELECT count(distinct(employee_record_id)) FROM
# `projapoti_db`.`user_login_history` where date(created) <= '2022-02-02'  and
# date(created) >= '2022-02-02' and is_mobile = 1;

from datetime import datetime, timedelta
from itertools import count

import pandas as pd
from backup_source_db.models import BackupDBLog, TrackBackupDBLastFetchTime
from dashboard_generate.models import ReportMobileAppUsersModel

from ...models import UserLoginHistory
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
        batch_objects.append(ReportMobileAppUsersModel(**object_dict))

        if len(batch_objects) >= 100:
            ReportMobileAppUsersModel.objects.bulk_create(batch_objects)
            batch_objects = []

    try:
        if batch_objects:
            ReportMobileAppUsersModel.objects.bulk_create(batch_objects)
    except Exception as e:
        pass

    return None


def querysets_to_dataframe_and_refine(request=None, *args, **kwargs):
    querysets = kwargs.get('querysets')
    querysets_values = querysets.values('employee_record_id', 'is_mobile', 'created')
    dataframe = pd.DataFrame(querysets_values)

    # convert created object to datetime
    dataframe['created'] = pd.to_datetime(dataframe['created'], errors='coerce')
    dataframe = dataframe.loc[~dataframe['created'].isnull(), :]
    dataframe = dataframe.loc[dataframe.is_mobile == 1, :]

    # generate date column
    dataframe['report_date'] = dataframe['created'].dt.date

    if not dataframe.empty:
        kwargs['dataframe'] = dataframe
        format_and_load_to_mysql_db(request, *args, **kwargs)


def get_user_login_history_querysets(*args, **kwargs):
    querysets = UserLoginHistory.objects.using('source_db').all()
    backup_log = BackupDBLog.objects.using('backup_source_db').last()

    try:
        last_login_history_time = backup_log.last_login_history_time
        if last_login_history_time:
            querysets = querysets.filter(created__gt=last_login_history_time)
        else:
            last_fetch_time = ReportMobileAppUsersModel.objects.last().report_day
            last_fetch_time = last_fetch_time + timedelta(days=1)
            querysets = querysets.filter(created__gte=last_fetch_time)
    except AttributeError:
        last_fetch_time = ReportMobileAppUsersModel.objects.last().report_day
        last_fetch_time = last_fetch_time + timedelta(days=1)
        querysets = querysets.filter(created__gte=last_fetch_time)

    return querysets


def generate_report(request=None, *args, **kwargs):
    print()
    print('start processing mobile_app_users report')

    querysets = get_user_login_history_querysets(request, *args, **kwargs)
    querysets = querysets.exclude(created__isnull=True)

    if querysets.exists():
        kwargs['querysets'] = querysets
        querysets_to_dataframe_and_refine(request, *args, **kwargs)

    print('End processing mobile_app_users report')
    print()

    return None
