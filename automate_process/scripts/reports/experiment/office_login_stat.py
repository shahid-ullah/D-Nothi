# experiment/office_login_stat.py
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
    values = objs.values('id', 'office_name', 'login_time')
    dataframe = pd.DataFrame(values)
    dataframe['login_time'] = dataframe.login_time.fillna(method='bfill')

    for date, login_time_frame in dataframe.groupby(
            dataframe.login_time.dt.date):
        sr = login_time_frame.groupby('office_name')['id'].count()
        office_name = sr.index
        office_values = sr.values
        inner_dict = {}
        for key, value in zip(office_name, office_values):
            key = key.strip(' ')
            inner_dict[key] = int(value)

        year = date.year
        month = date.month
        day = date.day

        if month < 10:
            month = single_digit_map[str(month)]
        if day < 10:
            day = single_digit_map[str(day)]

        primary_key = f"{year}{month}{day}"
        hour_map[primary_key] = inner_dict

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
            old_hour_map = object.office_login_map
            old_hour_map.update(hour_map)
            object.office_login_map = old_hour_map
            object.save()
        except AttributeError:
            object = LoginHistoryGraphsDataModel.objects.create()
            object.office_login_map = hour_map
            object.save()
    # office_login_frequenc = {}
    # for key, value in hour_map.items():
    #     for k, v in value.items():
    #         office_login_frequenc[k] = office_login_frequenc.setdefault(k,
    #                                                                     0) + v

    # x = dict(
    #     sorted(office_login_frequenc.items(), key=lambda x: x[1],
    #            reverse=True))

    # breakpoint()
    objs = None


generate_report()
