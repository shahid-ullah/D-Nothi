# automate_process/scripts/nispottikritto_nothi.py
# SELECT count(id) FROM nisponno_records where Date(operation_date) >= '2020-09-01' and Date(operation_date) <= '2020-09-30';
from datetime import datetime, timedelta

import pandas as pd

from automate_process.models import NisponnoRecords
from dashboard_generate.models import ReportNispottikrittoNothiModel


def generate_model_object_dict(request, report_date, count_or_sum, office_id, *args, **kwargs):
    object_dic = {}
    object_dic['year'] = report_date.year
    object_dic['month'] = report_date.month
    object_dic['day'] = report_date.day
    object_dic['year_month_day'] = str(report_date).replace('-', '')
    object_dic['report_date'] = str(report_date)
    object_dic['report_day'] = datetime(report_date.year, report_date.month, report_date.day)
    object_dic['count_or_sum'] = int(count_or_sum)
    object_dic['office_id'] = int(office_id)

    return object_dic


def format_and_load_to_mysql_db(request=None, *args, **kwargs):
    dataframe = kwargs['dataframe']

    grouped_report_date = dataframe.groupby(['office_id', 'report_date'], as_index=False, sort=False)['id'].size()
    batch_objects = []

    for office_id, report_date, counts in zip(
        grouped_report_date['office_id'].values,
        grouped_report_date['report_date'].values,
        grouped_report_date['size'].values,
    ):
        object_dict = generate_model_object_dict(request, report_date, counts, office_id, *args, **kwargs)
        batch_objects.append(ReportNispottikrittoNothiModel(**object_dict))

        if len(batch_objects) >= 100:
            ReportNispottikrittoNothiModel.objects.bulk_create(batch_objects)
            batch_objects = []

    if batch_objects:
        ReportNispottikrittoNothiModel.objects.bulk_create(batch_objects)

    return None


def querysets_to_dataframe_and_refine(request=None, *args, **kwargs):
    querysets = kwargs['querysets']

    querysets_values = querysets.values('id', 'office_id', 'type', 'upokarvogi', 'operation_date')
    dataframe = pd.DataFrame(querysets_values)

    # convert operation_date object to datetime
    dataframe['operation_date'] = pd.to_datetime(dataframe['operation_date'], errors='coerce')
    dataframe = dataframe.loc[~dataframe['operation_date'].isnull(), :]
    dataframe = dataframe.loc[~dataframe['office_id'].isnull(), :]

    # generate date column
    dataframe['report_date'] = dataframe['operation_date'].dt.date

    if not dataframe.empty:
        kwargs['dataframe'] = dataframe
        format_and_load_to_mysql_db(request, *args, **kwargs)

    return None


def get_nisponno_records_querysets(request, *args, **kwargs):
    querysets = kwargs['querysets']

    if querysets is not None:
        return querysets

    querysets = NisponnoRecords.objects.using('source_db').all()
    if ReportNispottikrittoNothiModel.objects.exists():
        last_fetch_time = ReportNispottikrittoNothiModel.objects.last().report_day
        last_fetch_time = last_fetch_time + timedelta(days=1)
        querysets = querysets.filter(created__gte=last_fetch_time)

    return querysets


def generate_report(request=None, *args, **kwargs):
    print()
    print('start processing nispottikritto_nothi report')

    querysets = get_nisponno_records_querysets(request, *args, **kwargs)
    querysets = querysets.exclude(created__isnull=True)

    if querysets.exists():
        kwargs['querysets'] = querysets
        querysets_to_dataframe_and_refine(request, *args, **kwargs)

    print('End processing nispottikritto_nothi report')
    print()

    return None
