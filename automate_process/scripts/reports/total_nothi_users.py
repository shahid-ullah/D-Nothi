# scripts/reports/total_nothi_users.py
# SELECT count(id) FROM users WHERE date(created) <= '2020-09-30';
from datetime import datetime, timedelta
import pandas as pd
from automate_process.models import Users
from . import utils

from dashboard_generate.models import ReportTotalUsersModel


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

    # groupby report_date
    grouped_report_date = dataframe.groupby(['report_date'], sort=False, as_index=False)['id'].size()
    batch_objects = []

    for report_date, nispottikritto_nothi_count in zip(grouped_report_date['report_date'].values, grouped_report_date['size'].values):
        object_dict = generate_model_object_dict(request, report_date, nispottikritto_nothi_count, *args, **kwargs)
        batch_objects.append(ReportTotalUsersModel(**object_dict))

        if len(batch_objects) >= 100:
            ReportTotalUsersModel.objects.bulk_create(batch_objects)
            batch_objects = []

    ReportTotalUsersModel.objects.bulk_create(batch_objects)

    return None

def querysets_to_dataframe_and_refine(request=None, *args, **kwargs):
    querysets = kwargs['querysets']

    querysets_values = querysets.values('id', 'created',)
    dataframe = pd.DataFrame(querysets_values)

    # convert created object to datetime
    dataframe['created'] = pd.to_datetime(dataframe.created, errors='coerce')
    dataframe = dataframe.loc[~dataframe.created.isnull(), :]

    # generate date column
    dataframe['report_date'] = dataframe['created'].dt.date

    if not dataframe.empty:
        kwargs['dataframe'] = dataframe
        format_and_load_to_mysql_db(request, *args, **kwargs)

    return None


def generate_report(request=None, *args, **kwargs):
    print()
    print('start processing total_nothi_users report')
    querysets = utils.get_users_querysets(*args, **kwargs)
    querysets = querysets.exclude(created__isnull=True)

    if querysets.exists():
        kwargs['querysets'] = querysets
        querysets_to_dataframe_and_refine(request, *args, **kwargs)

    print('End processing total_nothi_users report')
    print()
