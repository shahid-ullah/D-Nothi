# experiment/high_traffic_hours.py
import pandas as pd

from dashboard_generate.models import LoginHistoryGraphsDataModel

from ....models import UserLoginHistory


def first_ten_digit_map():
    single_digit_map = {}
    for i in range(0, 11):
        key1 = f"{i}"
        key2 = f"0{i}"
        value = f"0{i}"
        single_digit_map.setdefault(key1, value)
        single_digit_map.setdefault(key2, value)

    return single_digit_map


single_digit_map = first_ten_digit_map()


def generate_hour_map(objs):
    hour_map = {}
    values = objs.values('id', 'login_time')
    dataframe = pd.DataFrame(values)
    dataframe['login_time'] = dataframe.login_time.fillna(method='bfill')

    for date, login_time_frame in dataframe.groupby(
            dataframe.login_time.dt.date):

        for hour, hour_frame in login_time_frame.groupby(
                login_time_frame.login_time.dt.hour):

            year = date.year
            month = date.month
            day = date.day

            if month < 10:
                month = single_digit_map[str(month)]
            if day < 10:
                day = single_digit_map[str(day)]

            if hour < 10:
                hour = single_digit_map[str(hour)]

            key = f"{year}{month}{day}{hour}"
            hour_map[key] = hour_frame.shape[0]

    return hour_map


def generate_report():
    objs = UserLoginHistory.objects.using('source_db').all()[:]
    error = False
    hour_map = {}
    try:
        hour_map = generate_hour_map(objs)
    except Exception as e:
        error = True
        print(e)
    if not error:
        object = LoginHistoryGraphsDataModel.objects.last()
        try:
            old_hour_map = object.login_hour_map
            old_hour_map.update(hour_map)
            object.login_hour_map = old_hour_map
            object.save()
        except AttributeError:
            object = LoginHistoryGraphsDataModel.objects.create()
            object.login_hour_map = hour_map
            object.save()

    objs = None


generate_report()
