# scripts/reports/login_male_female_users.py
# SELECT count(DISTINCT(user_login_history.employee_record_id)) FROM
# `user_login_history` LEFT JOIN `employee_records` ON
# user_login_history.employee_record_id = employee_records.id WHERE
# employee_records.gender = 2 AND user_login_history.created >= '2022-01-01
# 00:00:00' AND user_login_history.created <= '2022-01-31 23:59:59';
from datetime import datetime

import numpy as np
import pandas as pd

from dashboard_generate.models import (ReportLoginFemalelUsersModel,
                                       ReportLoginMalelUsersModel)

from . import utils


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

def format_and_load_to_mysql_db(request=None, *args, **kwargs):
    dataframe = kwargs.get('dataframe')

    login_male_users_df = dataframe.loc[dataframe['gender'] == 1, :]
    login_female_users_df = dataframe.loc[dataframe['gender'] == 2, :]

    # groupby report_date
    male_grouped_report_date = login_male_users_df.groupby(['report_date'], sort=False, as_index=False).size()
    female_grouped_report_date = login_female_users_df.groupby(['report_date'], sort=False, as_index=False).size()

    batch_objects = []
    for report_date, male_count in zip(male_grouped_report_date['report_date'].values, male_grouped_report_date['size'].values):
        object_dict = generate_model_object_dict(request, report_date, male_count, *args, **kwargs)
        batch_objects.append(ReportLoginMalelUsersModel(**object_dict))

        if len(batch_objects) >= 100:
            ReportLoginMalelUsersModel.objects.bulk_create(batch_objects)
            batch_objects = []

    try:
        ReportLoginMalelUsersModel.objects.bulk_create(batch_objects)
    except Exception as e:
        pass

    batch_objects = []
    for report_date, female_count in zip(female_grouped_report_date['report_date'].values, female_grouped_report_date['size'].values):
        object_dict = generate_model_object_dict(request, report_date, female_count, *args, **kwargs)
        batch_objects.append(ReportLoginFemalelUsersModel(**object_dict))

        if len(batch_objects) >= 100:
            ReportLoginFemalelUsersModel.objects.bulk_create(batch_objects)
            batch_objects = []

    try:
        ReportLoginFemalelUsersModel.objects.bulk_create(batch_objects)
    except Exception as e:
        pass

    return None

def querysets_to_dataframe_and_refine(request=None, *args, **kwargs):
    login_history_querysets = kwargs['login_history_querysets']
    employee_querysets = kwargs['employee_querysets']

    login_history_querysets_values = login_history_querysets.values('employee_record_id', 'created')
    employee_querysets_values = employee_querysets.values('id', 'gender')

    login_history_dataframe = pd.DataFrame(login_history_querysets_values)
    employee_dataframe = pd.DataFrame(employee_querysets_values)

    # refine login history dataframe
    login_history_dataframe = login_history_dataframe.loc[~login_history_dataframe.created.isnull(), :]
    login_history_dataframe = login_history_dataframe.loc[~login_history_dataframe.employee_record_id.isnull(), :]
    login_history_dataframe = login_history_dataframe.astype({'employee_record_id': int})

    # refine employee_dataframe
    employee_dataframe = employee_dataframe.loc[~employee_dataframe['id'].isnull(), :]
    employee_dataframe = employee_dataframe.loc[~employee_dataframe['gender'].isnull(), :]
    employee_dataframe['gender'] = employee_dataframe['gender'].replace(r'^\s*$', np.nan, regex=True)
    employee_dataframe = employee_dataframe.loc[~employee_dataframe['gender'].isnull(), :]
    employee_dataframe = employee_dataframe.astype({'gender': int})
    employee_dataframe = employee_dataframe.astype({'id': int})

    dataframe = pd.merge(
        login_history_dataframe,
        employee_dataframe,
        how='left',
        left_on='employee_record_id',
        right_on='id',
        suffixes=('_login_history', '_employee_records'),
    )
    dataframe = dataframe.loc[~dataframe['gender'].isnull(), :]
    dataframe = dataframe.astype({'gender': int})
    dataframe = dataframe.loc[~dataframe['created'].isnull(), :]
    dataframe['created'] = pd.to_datetime(dataframe['created'], errors='coerce')
    dataframe = dataframe.loc[~dataframe['created'].isnull(), :]
    dataframe['report_date'] = dataframe['created'].dt.date

    if not dataframe.empty:
        kwargs['dataframe'] = dataframe
        format_and_load_to_mysql_db(request, *args, **kwargs)

    return None

def generate_report(request=None, *args, **kwargs):
    print()
    print('start processing login_male_female_users report')
    login_history_querysets = utils.get_user_login_history_querysets(*args, **kwargs)
    employee_querysets = utils.get_employee_records_querysets(*args, **kwargs)

    if login_history_querysets.exists() & employee_querysets.exists():
        kwargs['login_history_querysets'] = login_history_querysets
        kwargs['employee_querysets'] = employee_querysets
        querysets_to_dataframe_and_refine(request, *args, **kwargs)


    status = {}

    print('End processing login_male_female_users report')
    print()

    return status
