# SELECT count(id) FROM offices WHERE date(created) <= '2020-09-30' AND active_status =1;
# Caution: Datafame is not processed according to this query
# This is not cumulative count

from datetime import timedelta

import pandas as pd

from automate_process.models import Offices
from backup_source_db.models import TrackBackupDBLastFetchTime
from dashboard_generate.models import ReportTotalOfficesModel


def generate_object_map(report_date, number_of_offices, *args, **kwargs):
    object_dic = {}
    object_dic['year'] = report_date.year
    object_dic['month'] = report_date.month
    object_dic['day'] = report_date.day
    object_dic['report_date'] = str(report_date)
    object_dic['count_or_sum'] = int(number_of_offices)

    return object_dic


def format_and_load_to_mysql_db(request=None, *args, **kwargs):
    dataframe = kwargs['dataframe']

    # groupby report_date
    grouped_report_date = dataframe.groupby(['report_date'], sort=False, as_index=False)['id'].size()
    batch_objects = []

    batch_objects = []
    for report_date, office_count in zip(grouped_report_date['report_date'].values, grouped_report_date['size'].values):
        object_dic = generate_object_map(report_date, office_count)
        batch_objects.append(ReportTotalOfficesModel(**object_dic))

        if len(batch_objects) >= 100:
            ReportTotalOfficesModel.objects.bulk_create(batch_objects)
            batch_objects = []

    ReportTotalOfficesModel.objects.bulk_create(batch_objects)

    return None


def querysets_to_dataframe_and_refine(request=None, *args, **kwargs):
    querysets = kwargs.pop('querysets')
    queryset_values = querysets.values('id', 'active_status', 'created')
    dataframe = pd.DataFrame(queryset_values)

    # convert operation_date object to datetime
    dataframe['created'] = pd.to_datetime(dataframe['created'], errors='coerce')
    dataframe = dataframe.loc[~dataframe['created'].isnull(), :]
    dataframe = dataframe.astype({'active_status': int})
    dataframe = dataframe.loc[dataframe['active_status'] == 1, :]

    # generate date column
    dataframe['report_date'] = dataframe['created'].dt.date

    if not dataframe.empty:
        kwargs['dataframe'] = dataframe
        format_and_load_to_mysql_db(request, *args, **kwargs)

    return None

def get_offices_querysets(*args, **kwargs):
    last_fetch_time_object = TrackBackupDBLastFetchTime.objects.using('backup_source_db').last()
    querysets = Offices.objects.using('source_db').all()
    try:
        last_fetch_time = last_fetch_time_object.offices
        querysets = querysets.filter(created__gt=last_fetch_time)
    except AttributeError:
        last_fetch_time = ReportTotalOfficesModel.objects.last().report_date
        last_fetch_time = last_fetch_time + timedelta(days=1)
        querysets = querysets.filter(created__gte=last_fetch_time)

    return querysets

def generate_report(request=None, *args, **kwargs):
    print()
    print('start processing total_offices report')

    querysets = get_offices_querysets(*args, **kwargs)

    if querysets.exists():
        kwargs['querysets'] = querysets
        querysets_to_dataframe_and_refine(request, *args, **kwargs)

    print()
    print('End processing total_offices report')

    return None
