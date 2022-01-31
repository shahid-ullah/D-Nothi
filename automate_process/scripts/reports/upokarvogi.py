# SELECT count(id) FROM nisponno_records where Date(operation_date) >= '2020-09-01' and Date(operation_date) <= '2020-09-30';
import pandas as pd


def update(objs):

    print("Processing dataframe ...")
    # Extract mandatory attributes for offices graph analysis
    values = objs.values('id', 'upokarvogi', 'operation_date')
    dataframe = pd.DataFrame(values)
    # remove null values
    dataframe = dataframe.loc[dataframe.operation_date.notnull()]
    print(f"dataframe shape after removing operation_date null value {dataframe.shape}")
    # add new column: cretead_new as datetime field from operation_date column
    dataframe['opeation_date'] = pd.to_datetime(
        dataframe['operation_date'], errors='coerce'
    )
    # again remove null values based on opeation_date field
    dataframe = dataframe.loc[dataframe.opeation_date.notnull()]

    # Extract years and months from created column
    operation_date_datetime_index = pd.DatetimeIndex(dataframe['opeation_date'])
    years = operation_date_datetime_index.year.values.astype(str)
    months = operation_date_datetime_index.month.values.astype(str)
    days = operation_date_datetime_index.day.values.astype(str)
    dataframe['year'] = years
    dataframe['month'] = months
    dataframe['day'] = days

    dataframe_year_by = dataframe.groupby('year')
    year_data = []
    for year, year_frame in dataframe_year_by:
        year = str(year)
        year_dict = {}
        year_dict['year'] = year
        year_dict['count'] = int(year_frame['upokarvogi'].sum())
        year_dict['month_data'] = []

        month_data = []

        month_group_by = year_frame.groupby('month')
        for month, month_frame in month_group_by:
            month_dict = {}
            month_dict['month'] = month
            month_dict['count'] = int(month_frame['upokarvogi'].sum())
            month_dict['day_data'] = []

            day_data = []
            day_group_by = month_frame.groupby('day')
            for day, day_frame in day_group_by:
                day_dict = {}
                day_dict['day'] = day
                day_dict['count'] = int(day_frame['upokarvogi'].sum())
                day_data.append(day_dict)
            month_dict['day_data'] = day_data
            month_data.append(month_dict)

        year_dict['month_data'] = month_data
        if year_dict['count'] > 0:
            year_data.append(year_dict)

    dictionary = year_data

    return dictionary
