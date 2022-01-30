import json
import os

import pandas as pd
from django.conf import settings


def update():
    from ..models import UserLoginHistory

    if settings.DEBUG:
        objs = UserLoginHistory.objects.using('source_db').all()[:1000000]
    else:
        objs = UserLoginHistory.objects.using('source_db').all()

    try:
        values = objs.values('id', 'is_mobile', 'created')
        user_login_history_df = pd.DataFrame(values)

        user_login_history_df = user_login_history_df.loc[
            user_login_history_df.is_mobile == 1
        ]
        # remove null values
        user_login_history_df = user_login_history_df.loc[
            user_login_history_df.created.notnull()
        ]
        # add new column: cretead_new as datetime field from operation_date column
        user_login_history_df['created'] = pd.to_datetime(
            user_login_history_df['created'], errors='coerce'
        )
        user_login_history_df = user_login_history_df.loc[
            user_login_history_df.created.notnull()
        ]

        # Extract years and months from created column
        created_datetime_index = pd.DatetimeIndex(user_login_history_df['created'])
        years = created_datetime_index.year.values.astype(str)
        months = created_datetime_index.month.values.astype(str)
        days = created_datetime_index.day.values.astype(str)
        user_login_history_df['year'] = years
        user_login_history_df['month'] = months
        user_login_history_df['day'] = days
        print("Processing datframe completed ... \n")

        dataframe_year_by = user_login_history_df.groupby('year')

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

        dictionary = year_data

        dir_name = 'temporary_data'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        path = dir_name + "/" + "mobile_app_users.json"

        print("Saving graph data ...")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, ensure_ascii=False, indent=4)

        print("\nmobile_app_users.json ...")
        print("\nEnd of processing\n")
        return dictionary

    except Exception as e:
        print(e)
