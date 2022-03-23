# dashboard_generate/graph_methods.py
import itertools
import random

from .models import LoginHistoryGraphsDataModel


def hour_traffic():
    object = LoginHistoryGraphsDataModel.objects.last()
    login_maps = object.login_hour_map
    hour_map = {}

    for key, value in login_maps.items():
        hour = key[8:]
        hour_map[hour] = hour_map.setdefault(hour, 0) + value

    hour_map = {
        k: v
        for k, v in sorted(hour_map.items(), key=lambda item: item[0])
    }

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
    # breakpoint()

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
