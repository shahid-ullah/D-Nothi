from datetime import datetime

import pandas as pd

from dashboard_generate.models import (ReportFemaleNothiUsersModel,
                                       ReportMaleNothiUsersModel)


def update(request, users_objs, employee_objs, *args, **kwargs):
    # breakpoint()
    table_data = []
    report_date_list = []

    # START: GLOBAL SECTION

    day_map_dict = {}
    month_map_dict = {}

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

    def generate_year_month_day_key(year, month, day):
        year = str(year)
        month = str(month)
        month = month_map_dict[month]
        day = str(day)
        day = day_map_dict[day]
        year_month_day = year + month + day
        report_date = year + "-" + month + "-" + day
        report_date_list.append(year_month_day)
        # print(year_month_day)
        return year_month_day, report_date

    def generate_table_dictionary(year, month, day, count):
        year_month_day, report_date = generate_year_month_day_key(year, month, day)
        dict_ = {}
        dict_['year'] = year
        dict_['month'] = month
        dict_['day'] = day
        dict_['count_or_sum'] = count
        dict_['year_month_day'] = year_month_day
        dict_['report_date'] = report_date
        # breakpoint()
        if request.user.is_authenticated:
            dict_['creator'] = request.user
        # else:
        #     dict_['creator'] = request
        table_data.append(dict_)

        # print(dict_)
        return dict_

    def format_and_load_to_mysql_db_male(dataframe_year_by_male):
        print("loading male users data")
        # i = 0
        for year, year_frame in dataframe_year_by_male:
            # breakpoint()
            year = int(year)
            month_group_by = year_frame.groupby('month')
            for month, month_frame in month_group_by:
                month = int(month)

                day_group_by = month_frame.groupby('day')
                for day, day_frame in day_group_by:
                    day = int(day)
                    count = int(day_frame.shape[0])
                    # i = i + 1
                    # print(i)
                    report_day = datetime(year, month, day)

                    dict_ = generate_table_dictionary(year, month, day, count)
                    dict_['report_day'] = report_day
                    # print(year, month, day, count)
                    # print(dict_)
                    try:
                        obj = ReportMaleNothiUsersModel.objects.get(
                            year_month_day=dict_['year_month_day']
                        )
                        # for key, value in defaults.items():
                        #     setattr(obj, key, value)
                        # obj.save()
                    except ReportMaleNothiUsersModel.DoesNotExist:
                        obj = ReportMaleNothiUsersModel(**dict_)
                        obj.save()

    def format_and_load_to_mysql_db_female(dataframe_year_by):
        # breakpoint()
        # i = 0
        # breakpoint()
        for year, year_frame in dataframe_year_by:
            # breakpoint()
            year = int(year)
            month_group_by = year_frame.groupby('month')

            # if month_group_by.size() == 0:
            #     print('group size zero')

            for month, month_frame in month_group_by:
                month = int(month)

                day_group_by = month_frame.groupby('day')
                # if day_group_by.size() == 0:
                #     print('group size zero')

                for day, day_frame in day_group_by:
                    day = int(day)
                    count = int(day_frame.shape[0])
                    # i = i + 1
                    # print(i)
                    report_day = datetime(year, month, day)

                    dict_ = generate_table_dictionary(year, month, day, count)
                    dict_['report_day'] = report_day
                    # print(year, month, day, count)
                    # print(dict_)
                    try:
                        obj = ReportFemaleNothiUsersModel.objects.get(
                            year_month_day=dict_['year_month_day']
                        )
                        # for key, value in defaults.items():
                        #     setattr(obj, key, value)
                        # obj.save()
                    except ReportFemaleNothiUsersModel.DoesNotExist:
                        obj = ReportFemaleNothiUsersModel(**dict_)
                        obj.save()

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

    # users_dataframe.employee_record_id.astype('int', errors='ignore')
    # employee_records_dataframe.id.astype('int', errors='ignore')

    # remove null values

    print("Processing Dataframe ...")
    users_gender_df = pd.merge(
        users_dataframe,
        employee_records_dataframe,
        left_on=['employee_record_id'],
        right_on=['id'],
        suffixes=('_users', '_employee'),
    )
    # breakpoint()
    # breakpoint()
    # remove null values
    users_gender_df = users_gender_df.loc[users_gender_df.created_users.notnull()]
    # add new column: cretead_new as datetime field from created column
    users_gender_df['created_users'] = pd.to_datetime(
        users_gender_df['created_users'], errors='coerce'
    )
    users_gender_df = users_gender_df.loc[users_gender_df.created_users.notnull()]
    # breakpoint()
    users_gender_df = users_gender_df.astype({'gender': str})

    # Extract years and months from created column
    created_users_datetime_index = pd.DatetimeIndex(users_gender_df['created_users'])
    years = created_users_datetime_index.year.values.astype(str)
    months = created_users_datetime_index.month.values.astype(str)
    days = created_users_datetime_index.day.values.astype(str)

    users_gender_df['year'] = years
    users_gender_df['month'] = months
    users_gender_df['day'] = days

    print("End of Processing Dataframe ...")
    # breakpoint()

    male_nothi_users_df = users_gender_df[users_gender_df.gender == '1']
    female_nothi_users_df = users_gender_df[users_gender_df.gender != '1']
    # breakpoint()
    dataframe_year_by_male = male_nothi_users_df.groupby('year')
    format_and_load_to_mysql_db_male(dataframe_year_by_male)

    dataframe_year_by_female = female_nothi_users_df.groupby('year')
    format_and_load_to_mysql_db_female(dataframe_year_by_female)
