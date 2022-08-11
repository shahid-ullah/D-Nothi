# SELECT count(id) FROM offices WHERE date(created) <= '2020-09-30' AND active_status =1;
# Caution: Datafame is not processed according to this query
# This is not cumulative count
from datetime import datetime

import pandas as pd

from backup_source_db.models import BackupOffices
from dashboard_generate.models import ReportTotalOfficesModel


def generate_object_map(report_date, number_of_offices, *args, **kwargs):
    object_dic = {}
    object_dic['year'] = report_date.year
    object_dic['month'] = report_date.month
    object_dic['day'] = report_date.day
    object_dic['report_date'] = str(report_date)
    object_dic['count_or_sum'] = int(number_of_offices)

    return object_dic


def update(dataframe, request=None, *args, **kwargs):
    status = {}
    try:
        print()
        print('start processing total_offices report')
        groupby_date = dataframe.groupby(dataframe.created.dt.date)['id'].size()

        batch_objects = []
        for report_date, number_of_offices in zip(groupby_date.index, groupby_date.values):
            object_dic = generate_object_map(report_date, number_of_offices)
            batch_objects.append(ReportTotalOfficesModel(**object_dic))

            if len(batch_objects) >= 100:
                ReportTotalOfficesModel.objects.bulk_create(batch_objects)
                batch_objects = []

        ReportTotalOfficesModel.objects.bulk_create(batch_objects)

    except Exception as e:
        status['status'] = str(e)

    return status

def generate_report_total_offices(request=None, **kwargs):
    last_fetch_time_object = kwargs['last_fetch_time_object']
    current_fetch_time_map = kwargs['current_fetch_time_map']

    queryset = None
    last_fetch_time = None
    status = 'No new update'

    try:
        last_fetch_time = last_fetch_time_object.offices
        queryset = BackupOffices.objects.using('backup_source_db').filter(created__gt=last_fetch_time)
        queryset = queryset.exclude(created__isnull=True)

    except AttributeError:
        ReportTotalOfficesModel.objects.all().delete()
        queryset = BackupOffices.objects.using('backup_source_db').exclude(created__isnull=True)

    if queryset.exists():
        # update last_fetch_time
        last_fetch_time = queryset.last().created
        queryset_values = queryset.values('id', 'active_status', 'created')
        dataframe = pd.DataFrame(queryset_values)
        dataframe = dataframe.loc[dataframe.active_status == 1]
        if not dataframe.empty:
            status = update(dataframe, request, **kwargs)

    current_fetch_time_map['offices'] = last_fetch_time

    return current_fetch_time_map, status
