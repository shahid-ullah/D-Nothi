# dashboard_generate/graph_methods.py
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
