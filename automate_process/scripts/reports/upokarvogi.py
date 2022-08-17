# scripts/reports/upokarvogi.py
# SELECT SUM(upokarvogi) FROM nisponno_records where Date(operation_date) >= '2020-12-23' and Date(operation_date) <= '2020-23-24';
from datetime import datetime, timedelta

import pandas as pd
from . import utils

from automate_process.models import NisponnoRecords
from dashboard_generate.models import ReportUpokarvogiModel


def generate_model_object_dict(request, report_date, upokarvogi_sum, *args, **kwargs):
    object_dic = {}
    object_dic['year'] = report_date.year
    object_dic['month'] = report_date.month
    object_dic['day'] = report_date.day
    object_dic['year_month_day'] = str(report_date).replace('-', '')
    object_dic['report_date'] = str(report_date)
    object_dic['report_day'] = datetime(report_date.year, report_date.month, report_date.day)
    object_dic['count_or_sum'] = int(upokarvogi_sum)

    return object_dic

def format_and_load_to_mysql_db(request=None, *args, **kwargs):
    dataframe = kwargs['dataframe']
    # groupby report_date
    grouped_report_date = dataframe.groupby(['report_date'], sort=False, as_index=False)['upokarvogi'].sum()
    batch_objects = []

    for report_date, upokarvogi_sum in zip(grouped_report_date['report_date'].values, grouped_report_date['upokarvogi'].values):
        object_dict = generate_model_object_dict(request, report_date, upokarvogi_sum, *args, **kwargs)
        batch_objects.append(ReportUpokarvogiModel(**object_dict))

        if len(batch_objects) >= 100:
            ReportUpokarvogiModel.objects.bulk_create(batch_objects)
            batch_objects = []

    ReportUpokarvogiModel.objects.bulk_create(batch_objects)

def querysets_to_dataframe_and_refine(request=None, *args, **kwargs):
    querysets = kwargs.pop('querysets')
    querysets_values = querysets.values(
        'id', 'type', 'upokarvogi', 'operation_date'
    )
    dataframe = pd.DataFrame(querysets_values)

    # convert operation_date object to datetime
    dataframe['operation_date'] = pd.to_datetime(dataframe.operation_date, errors='coerce')
    dataframe = dataframe.loc[~dataframe.operation_date.isnull(), :]

    # generate date column
    dataframe['report_date'] = dataframe['operation_date'].dt.date

    if not dataframe.empty:
        kwargs['dataframe'] = dataframe
        format_and_load_to_mysql_db(request, *args, **kwargs)


def generate_report(request=None, *args, **kwargs):
    print()
    print('start processing upokarvogi report')

    querysets = utils.get_nisponno_records_querysets(*args, **kwargs)
    querysets = querysets.exclude(created__isnull=True)

    if querysets.exists():
        kwargs['querysets'] = querysets
        querysets_to_dataframe_and_refine(request, *args, **kwargs)

    print('End processing upokarvogi report')
    print()

    return 1, 2
