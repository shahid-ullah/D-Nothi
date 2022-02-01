import pandas as pd


def update(users_objs, employee_objs):

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

    users_dataframe.employee_record_id.astype('int', errors='ignore')
    employee_records_dataframe.id.astype('int', errors='ignore')

    # remove null values

    print("Processing Dataframe ...")
    users_gender_df = pd.merge(
        users_dataframe,
        employee_records_dataframe,
        left_on=['employee_record_id'],
        right_on=['id'],
        suffixes=('_users', '_employee'),
    )
    breakpoint()
    # remove null values
    users_gender_df = users_gender_df.loc[users_gender_df.created_users.notnull()]
    # add new column: cretead_new as datetime field from created column
    users_gender_df['created_users'] = pd.to_datetime(
        users_gender_df['created_users'], errors='coerce'
    )
    users_gender_df = users_gender_df.loc[users_gender_df.created_users.notnull()]

    # Extract years and months from created column
    created_users_datetime_index = pd.DatetimeIndex(users_gender_df['created_users'])
    years = created_users_datetime_index.year.values.astype(str)
    months = created_users_datetime_index.month.values.astype(str)
    days = created_users_datetime_index.day.values.astype(str)

    users_gender_df['year'] = years
    users_gender_df['month'] = months
    users_gender_df['day'] = days

    print("End of Processing Dataframe ...")

    male_nothi_users_df = users_gender_df[users_gender_df.gender == 1]
    # breakpoint()

    # # Generating Graph data (male users)

    # dataframe_year_by = male_nothi_users_df.groupby('year')

    # year_data = []
    # for year, year_frame in dataframe_year_by:
    #     year = str(year)
    #     # year, year_frame.shape
    #     year_dict = {}
    #     year_dict['year'] = year
    #     year_dict['count'] = int(year_frame.shape[0])
    #     year_dict['month_data'] = []

    #     month_data = []

    #     month_group_by = year_frame.groupby('month')
    #     for month, month_frame in month_group_by:
    #         month_dict = {}
    #         month_dict['month'] = month
    #         month_dict['count'] = month_frame.shape[0]
    #         month_dict['day_data'] = []

    #         day_data = []
    #         day_group_by = month_frame.groupby('day')
    #         for day, day_frame in day_group_by:
    #             day_dict = {}
    #             day_dict['day'] = day
    #             day_dict['count'] = day_frame.shape[0]
    #             day_data.append(day_dict)
    #         month_dict['day_data'] = day_data
    #         month_data.append(month_dict)

    #     year_dict['month_data'] = month_data
    #     year_data.append(year_dict)

    # male_nothi_users = year_data
    # # breakpoint()

    female_nothi_users_df = users_gender_df[users_gender_df.gender != 1]

    dataframe_year_by = female_nothi_users_df.groupby('year')

    year_data = []
    for year, year_frame in dataframe_year_by:
        year = str(year)
        # year, year_frame.shape
        year_dict = {}
        year_dict['year'] = year
        year_dict['count'] = int(year_frame.shape[0])
        year_dict['month_data'] = []

        month_data = []

        month_group_by = year_frame.groupby('month')
        for month, month_frame in month_group_by:
            month_dict = {}
            month_dict['month'] = month
            month_dict['count'] = month_frame.shape[0]
            month_dict['day_data'] = []

            day_data = []
            day_group_by = month_frame.groupby('day')
            for day, day_frame in day_group_by:
                day_dict = {}
                day_dict['day'] = day
                day_dict['count'] = day_frame.shape[0]
                day_data.append(day_dict)
            month_dict['day_data'] = day_data
            month_data.append(month_dict)

        year_dict['month_data'] = month_data
        year_data.append(year_dict)

    female_nothi_users = year_data

    return male_nothi_users, female_nothi_users
