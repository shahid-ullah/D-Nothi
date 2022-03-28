from datetime import datetime

import pandas as pd

from dashboard_generate.models import (ReportLoginFemalelUsersModel,
                                       ReportLoginMalelUsersModel)


def get_single_digit_maps():
    map = {}
    for i in range(0, 10):
        value = f"0{i}"
        map.setdefault(i, value)

    return map


SINGLE_DIGIT_KEY_MAPS = get_single_digit_maps()


def generate_year_month_day_key_and_report_date(year, month, day):
    if month < 10:
        month = SINGLE_DIGIT_KEY_MAPS[month]

    if day < 10:
        day = SINGLE_DIGIT_KEY_MAPS[day]
    year_month_day = f"{year}{month}{day}"
    report_date = f"{year}-{month}-{day}"

    return year_month_day, report_date


def generate_model_object_dictionary(request, year, month, day, count):
    year_month_day, report_date = generate_year_month_day_key_and_report_date(
        year, month, day)
    model_object_dict = {
        'year': year,
        'month': month,
        'day': day,
        'count_or_sum': count,
        'year_month_day': year_month_day,
        'report_date': report_date,
        'report_day': datetime(year, month, day)
    }
    try:
        if request.user.is_authenticated:
            model_object_dict['creator'] = request.user
    except Exception as e:
        pass

    return model_object_dict


def format_and_load_to_mysql_db(request, groupby_date, model):
    last_report_date = ''

    for date, frame in groupby_date:
        last_report_date = date

        count = frame['employee_record_id'].nunique()
        employee_ids = {}

        for id in frame.employee_record_id.values:
            employee_ids.setdefault(int(id), 1)

        dict_ = generate_model_object_dictionary(request, date.year,
                                                 date.month, date.day, count)
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


def update(request, user_login_history_dataframe, employee_records_dataframe,
           *args, **kwargs):
    try:
        print()
        print('start processing login male & female nothi users report')
        # user_login_history_dataframe = pd.DataFrame(user_login_history_values)
        # employee_records_dataframe = pd.DataFrame(employee_values)

        user_login_history_dataframe = user_login_history_dataframe.copy(
            deep=True)
        employee_records_dataframe = employee_records_dataframe.copy(deep=True)
        user_login_history_dataframe = user_login_history_dataframe[
            ~user_login_history_dataframe.employee_record_id.isnull()]
        user_login_history_dataframe = user_login_history_dataframe.astype(
            {'employee_record_id': int})

        employee_records_dataframe = employee_records_dataframe[
            ~employee_records_dataframe.id.isnull()]
        employee_records_dataframe = employee_records_dataframe.astype(
            {'id': int})
        dataframe = pd.merge(
            user_login_history_dataframe,
            employee_records_dataframe,
            how='left',
            left_on='employee_record_id',
            right_on='id',
            suffixes=('_login_history', '_employee_records'),
        )
        dataframe[
            'created_login_history'] = dataframe.created_login_history.fillna(
                method='bfill')
        dataframe = dataframe.astype({'gender': str})
        login_male_nothi_users_df = dataframe[dataframe.gender == '1']
        login_female_nothi_users_df = dataframe[dataframe.gender == '2']
        login_male_groupby_date = login_male_nothi_users_df.groupby(
            login_male_nothi_users_df.created_login_history.dt.date)
        login_male_last_report_date = format_and_load_to_mysql_db(
            request, login_male_groupby_date, ReportLoginMalelUsersModel)

        login_female_groupby_date = login_female_nothi_users_df.groupby(
            login_female_nothi_users_df.created_login_history.dt.date)
        login_female_last_report_date = format_and_load_to_mysql_db(
            request, login_female_groupby_date, ReportLoginFemalelUsersModel)

        print('End processing login male & female nothi users report')
        print()
    except Exception as e:
        login_male_last_report_date = str(e)
        login_female_last_report_date = str(e)
    return str(login_male_last_report_date), str(login_female_last_report_date)
