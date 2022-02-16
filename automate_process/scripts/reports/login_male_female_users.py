from datetime import datetime

import pandas as pd

from dashboard_generate.models import (ReportLoginFemalelUsersModel,
                                       ReportLoginMalelUsersModel)


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
        year, month, day
    )
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


def format_and_load_to_mysql_db(request, groupby_date, model):
    last_report_date = ''

    for date, frame in groupby_date:
        last_report_date = date

        count = frame['employee_record_id'].nunique()
        employee_ids = {}

        for id in frame.employee_record_id.values:
            employee_ids.setdefault(int(id), 1)

        dict_ = generate_model_object_dictionary(
            request, date.year, date.month, date.day, count
        )
        dict_['employee_record_ids'] = employee_ids
        defaults = {'count_or_sum': count, 'employee_record_ids': employee_ids}

        try:
            obj = model.objects.get(year_month_day=dict_['year_month_day'])
            for key, value in defaults.items():
                setattr(obj, key, value)
            obj.save()
        except model.DoesNotExist:
            obj = model(**dict_)
            obj.save()

    return last_report_date


def update(request, user_login_history_objs, employee_objs, *args, **kwargs):
    print()
    print('start processing login male & female nothi users report')
    user_login_history_values = user_login_history_objs.values(
        'employee_record_id',
        'created',
    )
    employee_records_values = employee_objs.values('id', 'gender')
    user_login_history_dataframe = pd.DataFrame(user_login_history_values)
    employee_records_dataframe = pd.DataFrame(employee_records_values)

    user_login_history_dataframe = user_login_history_dataframe[
        ~user_login_history_dataframe.employee_record_id.isnull()
    ]
    user_login_history_dataframe = user_login_history_dataframe.astype(
        {'employee_record_id': int}
    )

    employee_records_dataframe = employee_records_dataframe[
        ~employee_records_dataframe.id.isnull()
    ]
    employee_records_dataframe = employee_records_dataframe.astype({'id': int})
    dataframe = pd.merge(
        user_login_history_dataframe,
        employee_records_dataframe,
        how='left',
        left_on='employee_record_id',
        right_on='id',
        suffixes=('login_history', 'employee_records'),
    )
    dataframe['created'] = dataframe.created.fillna(method='bfill')
    dataframe = dataframe.astype({'gender': str})
    login_male_nothi_users_df = dataframe[dataframe.gender == '1']
    login_female_nothi_users_df = dataframe[dataframe.gender == '2']
    login_male_groupby_date = login_male_nothi_users_df.groupby(
        login_male_nothi_users_df.created.dt.date
    )
    login_male_last_report_date = format_and_load_to_mysql_db(
        request, login_male_groupby_date, ReportLoginMalelUsersModel
    )

    login_female_groupby_date = login_female_nothi_users_df.groupby(
        login_female_nothi_users_df.created.dt.date
    )
    login_female_last_report_date = format_and_load_to_mysql_db(
        request, login_female_groupby_date, ReportLoginFemalelUsersModel
    )

    print('End processing login male & female nothi users report')
    print()

    return login_male_last_report_date, login_female_last_report_date
