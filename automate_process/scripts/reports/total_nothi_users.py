# SELECT count(id) FROM users WHERE date(created) <= '2020-09-30';
import pandas as pd


def update(objs):

    values = objs.values('id', 'created')
    dataframe = pd.DataFrame(values)

    print("Processing Dataframe ...")
    # remove null values
    dataframe = dataframe.loc[dataframe.created.notnull()]
    # add new column: cretead_new as datetime field from created column
    dataframe['created'] = pd.to_datetime(dataframe['created'], errors='coerce')
    # again remove null values based on opeation_date field
    dataframe = dataframe.loc[dataframe.created.notnull()]

    # Extract years and months from created column
    created_datetime_index = pd.DatetimeIndex(dataframe['created'])
    years = created_datetime_index.year.values.astype(str)
    months = created_datetime_index.month.values.astype(str)
    days = created_datetime_index.day.values.astype(str)
    dataframe['year'] = years
    dataframe['month'] = months
    dataframe['day'] = days

    dataframe_year_by = dataframe.groupby('year')
    year_data = []
    for year, year_frame in dataframe_year_by:
        year = str(year)
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

    return dictionary
