import json
import time

import numpy as np
import pandas as pd
from django.db.models import Sum

from .models import (ReportAndroidUsersModel, ReportFemaleNothiUsersModel,
                     ReportIOSUsersModel, ReportLoginFemalelUsersModel,
                     ReportLoginMalelUsersModel, ReportLoginTotalUsers,
                     ReportMaleNothiUsersModel, ReportMobileAppUsersModel,
                     ReportNispottikrittoNothiModel, ReportNoteNisponnoModel,
                     ReportPotrojariModel, ReportTotalOfficesModel,
                     ReportTotalUsersModel, ReportUpokarvogiModel)

CACHED_DICTIONARY = {'last_cached': time.time()}


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def get_cache_or_calculate(report_type, mapping_method, model):
    global CACHED_DICTIONARY
    cached = CACHED_DICTIONARY.setdefault(report_type, {})
    if cached:
        last_cached = CACHED_DICTIONARY[report_type]['last_cached']
        current_time = time.time()
        if (current_time - last_cached) > (60 * 60):
            print('resetting cache')
            print()
            CACHED_DICTIONARY = {}
            objs = model.objects.all()
            CACHED_DICTIONARY.setdefault(report_type, {})
            year_map, month_map, day_map = mapping_method(objs)
            CACHED_DICTIONARY[report_type]['year_map'] = year_map
            CACHED_DICTIONARY[report_type]['month_map'] = month_map
            CACHED_DICTIONARY[report_type]['day_map'] = day_map
            CACHED_DICTIONARY[report_type]['last_cached'] = time.time()
        else:
            print('current time: ', current_time - last_cached)
            print('using cache')
            print()
            year_map = CACHED_DICTIONARY[report_type]['year_map']
            month_map = CACHED_DICTIONARY[report_type]['month_map']
            day_map = CACHED_DICTIONARY[report_type]['day_map']
    else:
        print('using raw calculation')
        print()
        objs = model.objects.all()
        CACHED_DICTIONARY.setdefault(report_type, {})
        year_map, month_map, day_map = mapping_method(objs)
        CACHED_DICTIONARY[report_type]['year_map'] = year_map
        CACHED_DICTIONARY[report_type]['month_map'] = month_map
        CACHED_DICTIONARY[report_type]['day_map'] = day_map
        CACHED_DICTIONARY[report_type]['last_cached'] = time.time()

    return year_map, month_map, day_map


def generate_year_month_and_day_map(objs):
    values = objs.values('year', 'month', 'day', 'count_or_sum')
    dataframe = pd.DataFrame(values)
    year_map = {}
    month_map = {}
    day_map = {}

    year_group_by = dataframe.groupby('year')
    for year, year_frame in year_group_by:
        year_map[year] = year_frame['count_or_sum'].sum()
        month_map[year] = {}
        day_map[year] = {}

        month_group_by = year_frame.groupby('month')

        for month, month_frame in month_group_by:
            month_map[year][month] = month_frame['count_or_sum'].sum()

            day_map[year][month] = {}

            day_group_by = month_frame.groupby('day')
            for day, day_frame in day_group_by:
                day_map[year][month][day] = day_frame['count_or_sum'].sum()

    return year_map, month_map, day_map


def generate_login_users_year_month_day_map(objs):
    values = objs.values('year', 'month', 'day', 'count_or_sum', 'employee_record_ids')
    dataframe = pd.DataFrame(values)
    year_map = {}
    month_map = {}
    day_map = {}

    for year, year_frame in dataframe.groupby('year'):
        year_dict = {}

        for ids_dict in year_frame['employee_record_ids'].values:
            year_dict.update(ids_dict)

        year_map[year] = len(year_dict)

        month_map[year] = {}
        day_map[year] = {}

        month_group_by = year_frame.groupby('month')

        for month, month_frame in month_group_by:
            month_dict = {}
            for ids_dict in month_frame['employee_record_ids'].values:
                month_dict.update(ids_dict)
            month_map[year][month] = len(month_dict)

            day_map[year][month] = {}

            day_group_by = month_frame.groupby('day')
            for day, day_frame in day_group_by:
                day_map[year][month][day] = day_frame['count_or_sum'].sum()

    return year_map, month_map, day_map


def get_total_office_count(date_range):
    offices_objs = ReportTotalOfficesModel.objects.filter(report_day__lte=date_range[1])
    office_count_dict = offices_objs.aggregate(Sum('count_or_sum'))
    office_count = office_count_dict['count_or_sum__sum']

    if not office_count:
        office_count = 0

    return office_count


def get_nispottikritto_nothi_count(date_range):
    nispottikritto_nothi_objects = ReportNispottikrittoNothiModel.objects.filter(
        report_day__range=date_range
    )
    nispottikritto_nothi_dict = nispottikritto_nothi_objects.aggregate(
        Sum('count_or_sum')
    )
    nispottikritto_nothi_count = nispottikritto_nothi_dict['count_or_sum__sum']

    if not nispottikritto_nothi_count:
        nispottikritto_nothi_count = 0

    return nispottikritto_nothi_count


def get_upokarvogi_count(date_range):
    upokarvogi_objects = ReportUpokarvogiModel.objects.filter(
        report_day__range=date_range
    )
    upokarvogi_dict = upokarvogi_objects.aggregate(Sum('count_or_sum'))
    upokarvogi = upokarvogi_dict['count_or_sum__sum']

    if not upokarvogi:
        upokarvogi = 0

    return upokarvogi


def get_potrojari_count(date_range):
    potrojari_objects = ReportPotrojariModel.objects.filter(
        report_day__range=date_range
    )
    potrojari_dict = potrojari_objects.aggregate(Sum('count_or_sum'))
    potrojari = potrojari_dict['count_or_sum__sum']

    if not potrojari:
        potrojari = 0

    return potrojari


def get_note_nisponno_count(date_range):
    note_nisponno_objects = ReportNoteNisponnoModel.objects.filter(
        report_day__range=date_range
    )
    note_nisponno_dict = note_nisponno_objects.aggregate(Sum('count_or_sum'))
    note_nisponno = note_nisponno_dict['count_or_sum__sum']

    if not note_nisponno:
        note_nisponno = 0

    return note_nisponno


def get_login_total_users(date_range):

    login_total_users_objects = ReportLoginTotalUsers.objects.filter(
        report_day__range=date_range
    )
    count_dict = {}
    for obj in login_total_users_objects:
        count_dict.update(obj.employee_record_ids)
    login_total_users = len(count_dict)
    if not login_total_users:
        login_total_users = 0

    return login_total_users


def get_login_male_users(date_range):
    login_male_users_objects = ReportLoginMalelUsersModel.objects.filter(
        report_day__range=date_range
    )
    count_dict = {}
    for obj in login_male_users_objects:
        count_dict.update(obj.employee_record_ids)
    login_male_users = len(count_dict)
    if not login_male_users:
        login_male_users = 0

    return login_male_users


def get_login_female_users(date_range):
    login_female_users_objects = ReportLoginFemalelUsersModel.objects.filter(
        report_day__range=date_range
    )
    count_dict = {}
    for obj in login_female_users_objects:
        count_dict.update(obj.employee_record_ids)
    login_female_users = len(count_dict)
    if not login_female_users:
        login_female_users = 0

    return login_female_users


def get_mobile_app_users(date_range):
    mobile_app_users_objects = ReportMobileAppUsersModel.objects.filter(
        report_day__range=date_range
    )
    mobile_app_users_dict = mobile_app_users_objects.aggregate(Sum('count_or_sum'))
    mobile_app_users = mobile_app_users_dict['count_or_sum__sum']

    if not mobile_app_users:
        mobile_app_users = 0

    return mobile_app_users


def get_total_users(date_range):
    total_users_objs = ReportTotalUsersModel.objects.filter(
        report_day__lte=date_range[1]
    )
    total_users_dict = total_users_objs.aggregate(Sum('count_or_sum'))
    total_users = total_users_dict['count_or_sum__sum']

    if not total_users:
        total_users = 0

    return total_users


def get_nothi_users_male(date_range):
    nothi_users_male_objs = ReportMaleNothiUsersModel.objects.filter(
        report_day__lte=date_range[1]
    )
    nothi_users_male_dict = nothi_users_male_objs.aggregate(Sum('count_or_sum'))
    nothi_users_male = nothi_users_male_dict['count_or_sum__sum']

    if not nothi_users_male:
        nothi_users_male = 0

    return nothi_users_male


def get_nothi_users_female(date_range):
    nothi_users_female_objs = ReportFemaleNothiUsersModel.objects.filter(
        report_day__lte=date_range[1]
    )
    nothi_users_female_dict = nothi_users_female_objs.aggregate(Sum('count_or_sum'))
    nothi_users_female = nothi_users_female_dict['count_or_sum__sum']

    if not nothi_users_female:
        nothi_users_female = 0

    return nothi_users_female
