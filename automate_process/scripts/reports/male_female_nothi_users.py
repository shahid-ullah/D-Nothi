from datetime import datetime

import pandas as pd

from dashboard_generate.models import (ReportFemaleNothiUsersModel,
                                       ReportMaleNothiUsersModel)


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

        count = frame['id_users'].count()

        dict_ = generate_model_object_dictionary(
            request, date.year, date.month, date.day, count
        )
        defaults = {'count_or_sum': count}

        try:
            obj = model.objects.get(year_month_day=dict_['year_month_day'])
            # obj = ReportTotalOfficesModel.objects.get(report_day=report_day)
            for key, value in defaults.items():
                setattr(obj, key, value)
            obj.save()
        except model.DoesNotExist:
            obj = model(**dict_)
            obj.save()
    return last_report_date


def update(request, users_objs, employee_objs, *args, **kwargs):
    print()
    print('start processing male & female nothi users report')
    users_values = users_objs.values(
        'id',
        'username',
        'user_role_id',
        'is_admin',
        'active',
        'user_status',
        'created',
        'modified',
        'employee_record_id',
    )
    employee_records_values = employee_objs.values(
        'id', 'name_eng', 'gender', 'created', 'modified'
    )
    users_dataframe = pd.DataFrame(users_values)
    employee_records_dataframe = pd.DataFrame(employee_records_values)

    users_dataframe = users_dataframe[~users_dataframe.employee_record_id.isnull()]
    users_dataframe = users_dataframe.astype({'employee_record_id': int})

    employee_records_dataframe = employee_records_dataframe[
        ~employee_records_dataframe.id.isnull()
    ]
    employee_records_dataframe = employee_records_dataframe.astype({'id': int})

    users_gender_df = pd.merge(
        users_dataframe,
        employee_records_dataframe,
        left_on=['employee_record_id'],
        right_on=['id'],
        suffixes=('_users', '_employee'),
    )
    users_gender_df = users_gender_df.loc[users_gender_df.created_users.notnull()]
    users_gender_df = users_gender_df.astype({'gender': str})

    male_nothi_users_df = users_gender_df[users_gender_df.gender == '1']
    female_nothi_users_df = users_gender_df[users_gender_df.gender != '1']

    male_groupby_date = male_nothi_users_df.groupby(
        male_nothi_users_df.created_users.dt.date
    )
    # breakpoint()
    male_last_report_date = format_and_load_to_mysql_db(
        request, male_groupby_date, ReportMaleNothiUsersModel
    )

    female_groupby_date = female_nothi_users_df.groupby(
        female_nothi_users_df.created_users.dt.date
    )
    female_last_report_date = format_and_load_to_mysql_db(
        request, female_groupby_date, ReportFemaleNothiUsersModel
    )

    print('End processing male & female nothi users report')
    print()

    return male_last_report_date, female_last_report_date