# dashboard_generate/graph_methods.py
import itertools
import random

from .models import LoginHistoryGraphsDataModel


def get_hour_maps():
    HOUR_MAPS = {
        '00': '12 AM',
        '01': '1 AM',
        '02': '2 AM',
        '03': '3 AM',
        '04': '4 AM',
        '05': '5 AM',
        '06': '6 AM',
        '07': '7 AM',
        '08': '8 AM',
        '09': '9 AM',
        '10': '10 AM',
        '11': '11 AM',
        '12': '12 PM',
        '13': '1 PM',
        '14': '2 PM',
        '15': '3 PM',
        '16': '4 PM',
        '17': '5 PM',
        '18': '6 PM',
        '19': '7 PM',
        '20': '8 PM',
        '21': '9 PM',
        '22': '10 PM',
        '23': '11 PM',
    }
    return HOUR_MAPS


def hour_traffic():
    object = LoginHistoryGraphsDataModel.objects.last()
    login_maps = object.login_hour_map
    hour_map = {}
    HOUR_MAPS = get_hour_maps()

    for key, value in login_maps.items():
        hour = key[8:]
        hour_map[hour] = hour_map.setdefault(hour, 0) + value

    hour_map = {
        k: v
        for k, v in sorted(hour_map.items(), key=lambda item: item[0])
    }
    hour_map = {HOUR_MAPS[k]: v for k, v in hour_map.items()}

    return hour_map


def day_traffic():
    object = LoginHistoryGraphsDataModel.objects.last()
    login_maps = object.login_hour_map
    hour_map = {}

    for key, value in login_maps.items():
        hour = key[6:8]
        hour_map[hour] = hour_map.setdefault(hour, 0) + value

    # hour_map = sorted(hour_map)
    hour_map = {
        k: v
        for k, v in sorted(hour_map.items(), key=lambda item: item[0])
    }

    return hour_map


def office_login_map():
    object = LoginHistoryGraphsDataModel.objects.last()
    login_maps = object.office_login_map

    office_login_frequenc = {}
    for key, value in login_maps.items():
        for k, v in value.items():
            office_login_frequenc[k] = office_login_frequenc.setdefault(k,
                                                                        0) + v

    office_login_frequenc = dict(
        sorted(office_login_frequenc.items(), key=lambda x: x[1],
               reverse=True))

    office_login_frequenc = dict(
        itertools.islice(office_login_frequenc.items(), 20))

    items = list(office_login_frequenc.items())
    random.shuffle(items)
    office_login_frequenc = dict(items)

    return office_login_frequenc
