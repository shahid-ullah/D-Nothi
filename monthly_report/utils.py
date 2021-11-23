# monthly_report/utils.py

import json

import numpy as np
import pandas as pd

from .models import CSVDataStorageModel, DataframeRecord

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
    '9': 'September',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December',
    'unknown': 'Unknown',
}


def load_csv(dataframe=None):
    csv_data = CSVDataStorageModel.objects.filter(dataframe=dataframe).first()
    dataframe = pd.read_csv(csv_data.file_name.path)

    return dataframe


def load_office_dataframe():
    print('loading offices dataframe ...')
    dataframe_object = DataframeRecord.objects.filter(dataframe_name='offices').first()
    dataframe = load_csv(dataframe_object)

    return dataframe


def load_nisponno_records_dataframe():
    print('loading nisponno_records dataframe ...')
    dataframe_object = DataframeRecord.objects.filter(
        dataframe_name='nisponno_records'
    ).first()
    dataframe = load_csv(dataframe_object)

    return dataframe


def load_users_dataframe():
    print('loading users dataframe ...')
    dataframe_object = DataframeRecord.objects.filter(dataframe_name='users').first()
    dataframe = load_csv(dataframe_object)

    return dataframe


def load_nothi_users_total_graph_data():

    print('loading users gender male dataframe ...')
    file_obj = load_file_object('total_users')
    file_content = load_file_content(file_obj)

    return generate_general_series_and_drilldown_series(file_content, 'years')


def load_users_gender_male_dataframe():
    print('loading users gender male dataframe ...')
    dataframe_object = DataframeRecord.objects.filter(
        dataframe_name='users_gender_male'
    ).first()
    dataframe = load_csv(dataframe_object)

    return dataframe


def load_file_object(file_name):
    file_obj_type = DataframeRecord.objects.filter(dataframe_name=file_name).first()
    file_obj = CSVDataStorageModel.objects.filter(dataframe=file_obj_type).first()

    return file_obj


def load_file_content(file_obj):

    with open(file_obj.file_name.path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    return data


def load_users_gender_male_graph_data():

    print('loading users gender male dataframe ...')
    file_obj = load_file_object('users_gender_male')
    file_content = load_file_content(file_obj)

    return generate_general_series_and_drilldown_series(file_content, 'years')


def load_users_gender_female_graph_data():

    print('loading users gender male dataframe ...')
    file_obj = load_file_object('users_gender_female')
    file_content = load_file_content(file_obj)

    return generate_general_series_and_drilldown_series(file_content, 'years')


def load_users_gender_female_dataframe():
    print('loading users gender female dataframe')
    dataframe_object = DataframeRecord.objects.filter(
        dataframe_name='users_gender_female'
    ).first()
    dataframe = load_csv(dataframe_object)

    return dataframe


def load_mobile_users_dataframe():
    print('loading users gender female dataframe ...')
    dataframe_object = DataframeRecord.objects.filter(
        dataframe_name='mobile_users'
    ).first()
    dataframe = load_csv(dataframe_object)

    return dataframe


def load_mobile_app_users_graph_data():

    print('loading mobile app users graph data ...')
    file_obj = load_file_object('mobile_app_users')
    file_content = load_file_content(file_obj)

    return generate_general_series_and_drilldown_series(file_content, 'years')


def load_total_nisponno_graph_data():

    print('loading total nisponno graph data ...')
    file_obj = load_file_object('total_nisponno')
    file_content = load_file_content(file_obj)

    return generate_general_series_and_drilldown_series(file_content, 'years')


def load_total_nisponno_dataframe():
    print('loading total_nisponno dataframe ...')
    dataframe_object = DataframeRecord.objects.filter(
        dataframe_name='total_nisponno'
    ).first()
    dataframe = load_csv(dataframe_object)

    return dataframe


def load_nispottikritto_nothi_graph_data():

    print('loading users gender male dataframe ...')
    file_obj = load_file_object('nispottikritto_nothi')
    file_content = load_file_content(file_obj)

    return generate_general_series_and_drilldown_series(file_content, 'years')


def load_potrojari_graph_data():

    print('loading potrojari graph data ...')
    file_obj = load_file_object('potrojari')
    file_content = load_file_content(file_obj)

    return generate_general_series_and_drilldown_series(file_content, 'years')


def load_potrojari_dataframe():
    print('loading potrojari dataframe ...')
    dataframe_object = DataframeRecord.objects.filter(
        dataframe_name='potrojari'
    ).first()
    dataframe = load_csv(dataframe_object)

    return dataframe


def load_upokarvogi_graph_data():

    print('loading total_upokarvogi graph data ...')
    file_obj = load_file_object('upokarvogi')
    file_content = load_file_content(file_obj)

    return generate_general_series_and_drilldown_series(file_content, 'years')


def load_total_upokarvogi_dateframe():
    print('loading total_upokarvogi dataframe ...')
    dataframe_object = DataframeRecord.objects.filter(
        dataframe_name='upokarvogi'
    ).first()
    dataframe = load_csv(dataframe_object)

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
        temporary_dict_general = {
            'name': year,
            'y': year_frame.shape[0],
            'drilldown': year,
        }
        general_series[0]['data'].append(temporary_dict_general)
        temporary_dict_drilldown = {
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

            temporary_dict_drilldown['data'].append(lst)
        drilldown_series.append(temporary_dict_drilldown)
    return general_series, drilldown_series


def upokarvogi_generate_general_series_drilldown_series(
    dataframe_year_by, general_series_name
):
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
        temporary_dict_general = {
            'name': year,
            'y': year_frame['upokarvogi'].sum(),
            'drilldown': year,
        }
        general_series[0]['data'].append(temporary_dict_general)
        temporary_dict_drilldown = {
            'name': year,
            'id': year,
            'data': [],
        }
        month_group_by = year_frame.groupby('month')
        for month, month_frame in month_group_by:

            # mg, mf.shape[0]
            month = str(month)
            month = month_map[month]
            lst = [month, month_frame['upokarvogi'].sum()]

            temporary_dict_drilldown['data'].append(lst)
        drilldown_series.append(temporary_dict_drilldown)
    return general_series, drilldown_series


def generate_general_series_and_drilldown_series(data, general_series_name):
    general_series = [
        {
            'name': general_series_name,
            'colorByPoint': True,
            'data': [],
        }
    ]
    drilldown_series = []
    for year in data:
        year = str(year)
        count = data[year]['count']
        month_map = data[year]['month_map']

        temporary_dict_general = {
            'name': year,
            'y': count,
            'drilldown': year,
        }
        general_series[0]['data'].append(temporary_dict_general)

        temporary_dict_drilldown = {
            'name': year,
            'id': year,
            'data': [],
        }
        for month in month_map:
            lst = [month, month_map[month]]
            temporary_dict_drilldown['data'].append(lst)
        drilldown_series.append(temporary_dict_drilldown)

    return general_series, drilldown_series
