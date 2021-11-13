# monthly_report/utils.py

import json

import numpy as np
import pandas as pd
from django.conf import settings

from .models import CSVDataStorageModel, TableNameModel

month_map = {
    '1': 'January',
    '01': 'January',
    '2': 'February',
    '02': 'February',
    '3': 'March',
    '03': 'March',
    '4': 'April',
    '04': 'April',
    '5': 'May',
    '05': 'May',
    '6': 'June',
    '06': 'June',
    '7': 'July',
    '07': 'July',
    '8': 'August',
    '08': 'August',
    '9': 'Septembr',
    '09': 'Septermber',
    '10': 'October',
    '11': 'November',
    '12': 'December',
    'unknown': 'Unknown',
}


def load_csv(table_name=None):
    csv_data = CSVDataStorageModel.objects.filter(table_name=table_name).first()
    dataframe = pd.read_csv(csv_data.file_name.path)

    return dataframe


def load_office_table():
    if not settings.OFFICES_CSV_FILE_LOADED:
        print('loading office table ...')
        table = TableNameModel.objects.filter(name='offices').first()
        path = load_csv(table)
        settings.OFFICES_CSV_FILE_PATH = path
        settings.OFFICES_CSV_FILE_LOADED = True


def load_nisponno_records_table():
    print('loading nisponno_records table ...')
    table = TableNameModel.objects.filter(name='nisponno_records').first()
    dataframe = load_csv(table)

    return dataframe


def load_users_table():
    print('loading users table ...')
    table = TableNameModel.objects.filter(name='users').first()
    dataframe = load_csv(table)

    return dataframe


def load_users_gender_male_table():
    print('loading users gender male table ...')
    table = TableNameModel.objects.filter(name='users_gender_male').first()
    dataframe = load_csv(table)

    return dataframe


def load_users_gender_female_table():
    print('loading users gender female table')
    table = TableNameModel.objects.filter(name='users_gender_female').first()
    dataframe = load_csv(table)

    return dataframe


def load_mobile_users_dataframe():
    print('loading users gender female table ...')
    table = TableNameModel.objects.filter(name='mobile_users').first()
    dataframe = load_csv(table)

    return dataframe


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def generate_general_series_drilldown_series(dataframe_year_by, general_series_name):
    general_series = [
        {
            'name': general_series_name,
            'colorByPoint': True,
            'data': [],
        }
    ]
    drilldown_series = []

    for year, year_frame in dataframe_year_by:
        year = str(year)
        # year, year_frame.shape
        t_dict_ge = {'name': year, 'y': year_frame.shape[0], 'drilldown': year}
        general_series[0]['data'].append(t_dict_ge)

        t_dict_dr = {
            'name': year,
            'id': year,
            'data': [],
        }
        month_group_by = year_frame.groupby('month')
        for month, month_frame in month_group_by:
            # mg, mf.shape[0]
            month = str(month)
            month = month_map[month]

            lst = [month, month_frame.shape[0]]
            t_dict_dr['data'].append(lst)
            drilldown_series.append(t_dict_dr)
    return general_series, drilldown_series
