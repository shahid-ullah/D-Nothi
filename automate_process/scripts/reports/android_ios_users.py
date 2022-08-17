# scripts/reports/android_ios_users.py
from datetime import datetime, timedelta

import pandas as pd
from . import utils

from dashboard_generate.models import (ReportAndroidUsersModel,
                                       ReportIOSUsersModel)


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
    dataframe_android = dataframe.loc[dataframe['device_type'] == 'android', :]
    dataframe_ios = dataframe.loc[dataframe['device_type'] == 'ios', :]

    # groupby report_date
    android_grouped_report_date = dataframe_android.groupby(['report_date'], sort=False, as_index=False).size()
    ios_grouped_report_date = dataframe_ios.groupby(['report_date'], sort=False, as_index=False).size()

    batch_objects = []
    for report_date, andorid_count in zip(android_grouped_report_date['report_date'].values, android_grouped_report_date['size'].values):
        object_dict = generate_model_object_dict(request, report_date, andorid_count, *args, **kwargs)
        batch_objects.append(ReportAndroidUsersModel(**object_dict))

        if len(batch_objects) >= 100:
            ReportAndroidUsersModel.objects.bulk_create(batch_objects)
            batch_objects = []

    try:
        ReportAndroidUsersModel.objects.bulk_create(batch_objects)
    except Exception as e:
        pass

    batch_objects = []
    for report_date, ios_count in zip(ios_grouped_report_date['report_date'].values, ios_grouped_report_date['size'].values):
        object_dict = generate_model_object_dict(request, report_date, ios_count, *args, **kwargs)
        batch_objects.append(ReportIOSUsersModel(**object_dict))

        if len(batch_objects) >= 100:
            ReportIOSUsersModel.objects.bulk_create(batch_objects)
            batch_objects = []

    try:
        ReportIOSUsersModel.objects.bulk_create(batch_objects)
    except Exception as e:
        pass

    return None


def querysets_to_dataframe_and_refine(request=None, *args, **kwargs):
    querysets = kwargs.get('querysets')
    querysets_values = querysets.values('device_type', 'is_mobile', 'created')
    dataframe = pd.DataFrame(querysets_values)

    dataframe = dataframe.astype({'is_mobile': int})
    dataframe = dataframe.astype({'device_type': str})
    dataframe['device_type'] = dataframe['device_type'].str.lower()

    dataframe = dataframe.loc[dataframe.is_mobile == 1, :]

    # convert created object to datetime
    dataframe['created'] = pd.to_datetime(dataframe['created'], errors='coerce')
    dataframe = dataframe.loc[~dataframe['created'].isnull(), :]

    # generate date column
    dataframe['report_date'] = dataframe['created'].dt.date
    # breakpoint()

    if not dataframe.empty:
        kwargs['dataframe'] = dataframe
        format_and_load_to_mysql_db(request, *args, **kwargs)


def generate_report(request=None, *args, **kwargs):
    print()
    print('start processing android & ios users report')

    querysets = utils.get_user_login_history_querysets(*args, **kwargs)
    querysets = querysets.exclude(created__isnull=True)

    if querysets.exists():
        kwargs['querysets'] = querysets
        querysets_to_dataframe_and_refine(request, *args, **kwargs)

    print('End processing android & ios users report')
    print()

    return None