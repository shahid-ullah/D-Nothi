from datetime import datetime

import pandas as pd

from dashboard_generate.models import (ReportFemaleNothiUsersModel,
                                       ReportMaleNothiUsersModel)


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

        count = frame['id_users'].count()

        dict_ = generate_model_object_dictionary(request, date.year,
                                                 date.month, date.day, count)
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


def update(request, users_dataframe, employee_records_dataframe, *args,
           **kwargs):
    status = {}
    status['male_nothi_users'] = {}
    status['female_nothi_users'] = {}
    try:
        users_dataframe = users_dataframe.copy(deep=True)
        employee_records_dataframe = employee_records_dataframe.copy(deep=True)
        print()
        print('start processing male & female nothi users report')
        # users_dataframe = pd.DataFrame(user_values)
        # employee_records_dataframe = pd.DataFrame(employee_values)

        users_dataframe = users_dataframe[~users_dataframe.employee_record_id.
                                          isnull()]
        users_dataframe = users_dataframe.astype({'employee_record_id': int})

        employee_records_dataframe = employee_records_dataframe[
            ~employee_records_dataframe.id.isnull()]
        employee_records_dataframe = employee_records_dataframe.astype(
            {'id': int})

        users_gender_df = pd.merge(
            users_dataframe,
            employee_records_dataframe,
            left_on=['employee_record_id'],
            right_on=['id'],
            suffixes=('_users', '_employee'),
        )
        users_gender_df[
            'created_users'] = users_gender_df.created_users.fillna(
                method='bfill')

        users_gender_df = users_gender_df.astype({'gender': str})

        male_nothi_users_df = users_gender_df[users_gender_df.gender == '1']
        female_nothi_users_df = users_gender_df[users_gender_df.gender == '2']

        male_groupby_date = male_nothi_users_df.groupby(
            male_nothi_users_df.created_users.dt.date)
        male_last_report_date = format_and_load_to_mysql_db(
            request, male_groupby_date, ReportMaleNothiUsersModel)

        female_groupby_date = female_nothi_users_df.groupby(
            female_nothi_users_df.created_users.dt.date)
        female_last_report_date = format_and_load_to_mysql_db(
            request, female_groupby_date, ReportFemaleNothiUsersModel)

        print('End processing male & female nothi users report')
        print()

        status['male_nothi_users']['last_report_date'] = str(
            male_last_report_date)
        status['female_nothi_users']['last_report_date'] = str(
            female_last_report_date)
        status['status'] = 'success'
    except Exception as e:
        status['status'] = str(e)

    return status
