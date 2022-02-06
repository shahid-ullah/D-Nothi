from datetime import datetime

import pandas as pd

from dashboard_generate.models import ReportPotrojariModel


def update(objs, request=None, *args, **kwargs):
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

    def format_and_load_to_mysql_db(dataframe_year_by):
        # i = 0
        for year, year_frame in dataframe_year_by:
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
                        obj = ReportPotrojariModel.objects.get(
                            year_month_day=dict_['year_month_day']
                        )
                        # for key, value in defaults.items():
                        #     setattr(obj, key, value)
                        # obj.save()
                    except ReportPotrojariModel.DoesNotExist:
                        obj = ReportPotrojariModel(**dict_)
                        obj.save()

    step = 1000
    start_index = 0
    end_index = start_index + step

    values = objs.values('id', 'type', 'operation_date')

    while True:
        new_values = values[start_index:end_index]
        start_index = end_index
        end_index = start_index + step

        if not new_values.exists():
            break
        dataframe = pd.DataFrame(new_values)

        dataframe = dataframe.loc[dataframe.type == 'potrojari']
        # remove null values
        dataframe = dataframe.loc[dataframe.operation_date.notnull()]
        # add new column: cretead_new as datetime field from operation_date column
        dataframe['operation_date'] = pd.to_datetime(
            dataframe['operation_date'], errors='coerce'
        )
        # again remove null values based on opeation_date field
        dataframe = dataframe.loc[dataframe.operation_date.notnull()]
        # Extract years and months from created column
        operation_date_datetime_index = pd.DatetimeIndex(dataframe['operation_date'])
        years = operation_date_datetime_index.year.values.astype(str)
        months = operation_date_datetime_index.month.values.astype(str)
        days = operation_date_datetime_index.day.values.astype(str)
        dataframe['year'] = years
        dataframe['month'] = months
        dataframe['day'] = days

        dataframe_year_by = dataframe.groupby('year')
        format_and_load_to_mysql_db(dataframe_year_by)
