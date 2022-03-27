# SELECT count(id) FROM users WHERE date(created) <= '2020-09-30';
from datetime import datetime

import pandas as pd

from dashboard_generate.models import ReportTotalUsersModel


def initialize_day_map():
    day_map_dict = {}
    for i in range(32):
        if i < 10:
            key1 = str(i)
            key2 = '0' + str(i)
            value = '0' + str(i)
            day_map_dict.setdefault(key1, value)
            day_map_dict.setdefault(key2, value)
        else:
            key = str(i)
            value = str(i)
            day_map_dict.setdefault(key, value)

    return day_map_dict


def initialize_month_map():
    month_map_dict = {}
    for i in range(13):
        if i < 10:
            key1 = str(i)
            key2 = '0' + str(i)
            value = '0' + str(i)
            month_map_dict.setdefault(key1, value)
            month_map_dict.setdefault(key2, value)
        else:
            key = str(i)
            value = str(i)
            month_map_dict.setdefault(key, value)
    return month_map_dict


DAY_MAP_DICT = initialize_day_map()
MONTH_MAP_DICT = initialize_month_map()


def generate_year_month_day_key_and_report_date(year, month, day):
    year = str(year)
    month = str(month)
    day = str(day)

    month = MONTH_MAP_DICT[month]
    day = DAY_MAP_DICT[day]

    year_month_day = year + month + day
    report_date = year + "-" + month + "-" + day

    return year_month_day, report_date


def generate_model_object_dictionary(request, year, month, day, count):
    year_month_day, report_date = generate_year_month_day_key_and_report_date(
        year, month, day)
    dict_ = {}
    dict_['year'] = year
    dict_['month'] = month
    dict_['day'] = day
    dict_['count_or_sum'] = count
    dict_['year_month_day'] = year_month_day
    dict_['report_date'] = report_date
    report_day = datetime(year, month, day)

    dict_['report_day'] = report_day

    try:
        if request.user.is_authenticated:
            dict_['creator'] = request.user
    except Exception as e:
        pass

    return dict_


def format_and_load_to_mysql_db(request, groupby_date):
    last_report_date = ''

    for date, frame in groupby_date:
        last_report_date = date

        count = frame['id'].count()

        dict_ = generate_model_object_dictionary(request, date.year,
                                                 date.month, date.day, count)
        defaults = {'count_or_sum': count}

        try:
            obj = ReportTotalUsersModel.objects.get(
                year_month_day=dict_['year_month_day'])
            # obj = ReportTotalOfficesModel.objects.get(report_day=report_day)
            for key, value in defaults.items():
                setattr(obj, key, value)
            obj.save()
        except ReportTotalUsersModel.DoesNotExist:
            obj = ReportTotalUsersModel(**dict_)
            obj.save()
    return last_report_date


def update(values, request=None, *args, **kwags):
    status = {}
    try:
        print()
        print('start processing total_nothi_users report')

        # values = objs.values('id', 'created')

        dataframe = pd.DataFrame(values)

        # dataframe = dataframe.loc[dataframe.created.notnull()]

        dataframe['created'] = dataframe.created.fillna(method='bfill')

        groupby_date = dataframe.groupby(dataframe.created.dt.date)

        last_report_date = format_and_load_to_mysql_db(request, groupby_date)
        print('End processing total_nothi_users report')
        print()
        status['last_report_date'] = str(last_report_date)
        status['status'] = 'success'
    except Exception as e:
        status['status'] = str(e)
        status['last_report_date'] = []

    return status
