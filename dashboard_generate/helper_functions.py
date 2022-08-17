# dashboard_generate/helper_functions.py
import json
import time
from datetime import date

import numpy as np
import pandas as pd
from django.db.models import Sum

from .models import (ReportAndroidUsersModel, ReportFemaleNothiUsersModel,
                     ReportIOSUsersModel, ReportLoginFemalelUsersModel,
                     ReportLoginMalelUsersModel, ReportLoginTotalUsers, ReportLoginTotalUsersNotDistinct,
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


MONTH_MAP = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}


def get_report_summary_count():

    today = date.today()
    year = today.year
    month = today.month

    report_summary_count = {}

    # office_total calculate
    try:
        office_count_dict = ReportTotalOfficesModel.objects.aggregate(Sum('count_or_sum'))
        office_total = int(office_count_dict['count_or_sum__sum'])

        if not office_total:
            office_total = 0
    except Exception as _:
        office_total = 0

    # users total calculate
    try:
        users_total_dict = ReportTotalUsersModel.objects.aggregate(Sum('count_or_sum'))
        users_total = int(users_total_dict['count_or_sum__sum'])

        if not users_total:
            users_total = 0
    except Exception as _:
        users_total = 0

    # male users total calculate
    try:
        nothi_users_male_dict = ReportMaleNothiUsersModel.objects.aggregate(
            Sum('count_or_sum'))
        male_users_total = int(nothi_users_male_dict['count_or_sum__sum'])

        if not male_users_total:
            male_users_total = 0
    except Exception as _:
        male_users_total = 0

    # female users total calculate
    try:
        nothi_users_female_dict = ReportFemaleNothiUsersModel.objects.aggregate(
            Sum('count_or_sum'))
        female_users_total = int(nothi_users_female_dict['count_or_sum__sum'])

        if not female_users_total:
            female_users_total = 0
    except Exception as _:
        female_users_total = 0

    # login users total calculate for current month
    try:
        login_total_users_objects = ReportLoginTotalUsers.objects.filter(
            year=year, month=month)
        login_total_users_dict = login_total_users_objects.aggregate(
            Sum('count_or_sum'))
        login_users_total = int(login_total_users_dict['count_or_sum__sum'])
        if not login_users_total:
            login_users_total = 0
    except Exception as _:
        login_users_total = 0

    # login male users total calculate for current month
    try:
        login_male_users_objects = ReportLoginMalelUsersModel.objects.filter(
            year=year, month=month)
        login_male_users_dict = login_male_users_objects.aggregate(
            Sum('count_or_sum'))
        login_male_users_total = int(login_male_users_dict['count_or_sum__sum'])
        if not login_male_users_total:
            login_male_users_total = 0
    except Exception as _:
        login_male_users_total = 0

    # login female users total calculate for current month
    try:
        login_female_users_objects = ReportLoginFemalelUsersModel.objects.filter(
            year=year, month=month)
        login_female_users_dict = login_female_users_objects.aggregate(
            Sum('count_or_sum'))
        female_login_users_total = int(login_female_users_dict['count_or_sum__sum'])
        if not female_login_users_total:
            female_login_users_total = 0
    except Exception as _:
        female_login_users_total = 0

    # nispottikritto_nothi total calculate for current month
    try:
        nispottikritto_nothi_objects = ReportNispottikrittoNothiModel.objects.filter(
            year=year, month=month)
        nispottikritto_nothi_dict = nispottikritto_nothi_objects.aggregate(
            Sum('count_or_sum'))
        nispottikritto_nothi_count = int(nispottikritto_nothi_dict['count_or_sum__sum'])
        if not nispottikritto_nothi_count:
            nispottikritto_nothi_count = 0
    except Exception as _:
        nispottikritto_nothi_count = 0

    # upokarvogi total calculate for current month
    try:
        upokarvogi_objects = ReportUpokarvogiModel.objects.filter(year=year,
                                                                  month=month)
        upokarvogi_dict = upokarvogi_objects.aggregate(Sum('count_or_sum'))
        upokarvogi = int(upokarvogi_dict['count_or_sum__sum'])
        if not upokarvogi:
            upokarvogi = 0
    except Exception as _:
        upokarvogi = 0

    # potrojari total calculate for current month
    try:
        potrojari_objects = ReportPotrojariModel.objects.filter(year=year,
                                                                month=month)
        potrojari_dict = potrojari_objects.aggregate(Sum('count_or_sum'))
        potrojari = int(potrojari_dict['count_or_sum__sum'])
        if not potrojari:
            potrojari = 0
    except Exception as _:
        potrojari = 0

    # note nisponno total calculate for current month
    try:
        note_nisponno_objects = ReportNoteNisponnoModel.objects.filter(year=year,
                                                                       month=month)
        note_nisponno_dict = note_nisponno_objects.aggregate(Sum('count_or_sum'))
        note_nisponno = int(note_nisponno_dict['count_or_sum__sum'])
        if not note_nisponno:
            note_nisponno = 0
    except Exception as _:
        note_nisponno = 0

    # mobile app users total calculate for current month
    try:
        mobile_app_users_objects = ReportMobileAppUsersModel.objects.filter(
            year=year, month=month)
        mobile_app_users_dict = mobile_app_users_objects.aggregate(
            Sum('count_or_sum'))
        mobile_app_users = int(mobile_app_users_dict['count_or_sum__sum'])
        if not mobile_app_users:
            mobile_app_users = 0
    except Exception as _:
        mobile_app_users = 0

    report_summary_count['office_total'] = office_total
    report_summary_count['users_total'] = users_total
    report_summary_count['male_users_total'] = male_users_total
    report_summary_count['female_users_total'] = female_users_total
    report_summary_count['login_users'] = login_users_total
    report_summary_count['male_login_users'] = login_male_users_total
    report_summary_count['female_login_users'] = female_login_users_total
    report_summary_count['nispottikritto_nothi'] = nispottikritto_nothi_count
    report_summary_count['note_nisponno'] = note_nisponno
    report_summary_count['potrojari'] = potrojari
    report_summary_count['upokarvogi'] = upokarvogi
    report_summary_count['mobile_app_users'] = mobile_app_users

    return report_summary_count

def generate_login_stack_bar_chart_data():

    try:
        login_male_objs = ReportLoginMalelUsersModel.objects.all()
        login_female_objs = ReportLoginFemalelUsersModel.objects.all()

        login_male_values = login_male_objs.values()
        login_female_values = login_female_objs.values()

        login_male_df = pd.DataFrame(login_male_values)
        login_female_df = pd.DataFrame(login_female_values)
        login_male_df = login_male_df.sort_values(by='report_day', ascending=False)
        login_female_df = login_female_df.sort_values(by='report_day', ascending=False)

        login_male_groups = login_male_df.groupby([login_male_df.report_day.dt.year, login_male_df.report_day.dt.month], sort=False)
        login_female_groups = login_female_df.groupby([login_female_df.report_day.dt.year, login_female_df.report_day.dt.month], sort=False)

        male_list = []
        female_list = []

        max_months_result = 5
        months = []

        count = 1

        for gr, frame in login_male_groups:
            if count > max_months_result:
                break

            month = MONTH_MAP[int(gr[1])]
            x = f'{gr[0]} {month}'

            temporary_dic = {}
            for value in frame.employee_record_ids.values:
                temporary_dic.update(value)

            male_list.append(len(temporary_dic))
            months.append(x)
            count = count + 1

        count = 1
        for gr, frame in login_female_groups:
            if count > max_months_result:
                break
            x = f'{gr[0]}_{gr[1]}'
            temporary_dic = {}
            for value in frame.employee_record_ids.values:
                temporary_dic.update(value)
            female_list.append(len(temporary_dic))
            count = count + 1

        chart_data_map = {'male_list': male_list, 'female_list': female_list, 'months': months}
    except Exception as _:
        chart_data_map = {'male_list': [], 'female_list': [], 'months': []}

    return chart_data_map


def generate_nispottikritto_nothi_plot_data():
    try:
        objs_nispottikritto_nothi = ReportNispottikrittoNothiModel.objects.all()
        values_nispottikritto_nothi = objs_nispottikritto_nothi.values('count_or_sum', 'report_day')

        df_nispottikritto_nothi = pd.DataFrame(values_nispottikritto_nothi)
        df_nispottikritto_nothi= df_nispottikritto_nothi.sort_values(by='report_day', ascending=False)
        year_group_sum_nispottikritto_nothi= df_nispottikritto_nothi.groupby(df_nispottikritto_nothi.report_day.dt.year, sort=False)['count_or_sum'].sum()
        years = [int(year) for year in year_group_sum_nispottikritto_nothi.index][:5]
        values = [int(value) for value in year_group_sum_nispottikritto_nothi.values][:5]
        percentages = [round(value*100/sum(values)) for value in values][:5]
        nispottikritto_nothi_plot_data = [{'year': year, 'value': value, 'percentage': percentage} for year, value, percentage in zip(years, values, percentages)]
    except Exception as _:
        nispottikritto_nothi_plot_data = [{}]

    return nispottikritto_nothi_plot_data


def get_cache_or_calculate(report_type, mapping_method, model):
    global CACHED_DICTIONARY
    cached = CACHED_DICTIONARY.setdefault(report_type, {})
    if cached:
        last_cached = CACHED_DICTIONARY[report_type]['last_cached']
        current_time = time.time()
        if (current_time - last_cached) > (1 * 60):
            # print('resetting cache')
            # print()
            CACHED_DICTIONARY = {}
            objs = model.objects.all()
            CACHED_DICTIONARY.setdefault(report_type, {})
            year_map, month_map, day_map = mapping_method(objs)
            CACHED_DICTIONARY[report_type]['year_map'] = year_map
            CACHED_DICTIONARY[report_type]['month_map'] = month_map
            CACHED_DICTIONARY[report_type]['day_map'] = day_map
            CACHED_DICTIONARY[report_type]['last_cached'] = time.time()
        else:
            # print('current time: ', current_time - last_cached)
            # print('using cache')
            # print()
            year_map = CACHED_DICTIONARY[report_type]['year_map']
            month_map = CACHED_DICTIONARY[report_type]['month_map']
            day_map = CACHED_DICTIONARY[report_type]['day_map']
    else:
        # print('using raw calculation')
        # print()
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
        year_map[year] = int(year_frame['count_or_sum'].sum())
        month_map[year] = {}
        day_map[year] = {}

        month_group_by = year_frame.groupby('month')

        for month, month_frame in month_group_by:
            month_map[year][month] = int(month_frame['count_or_sum'].sum())

            day_map[year][month] = {}

            day_group_by = month_frame.groupby('day')
            for day, day_frame in day_group_by:
                day_map[year][month][day] = int(day_frame['count_or_sum'].sum())

    return year_map, month_map, day_map


def generate_login_users_year_month_day_map(objs):
    values = objs.values('year', 'month', 'day', 'count_or_sum',
                         'employee_record_ids')
    dataframe = pd.DataFrame(values)
    year_map = {}
    month_map = {}
    day_map = {}

    for year, year_frame in dataframe.groupby('year'):
        year = int(year)
        year_dict = {}

        for ids_dict in year_frame['employee_record_ids'].values:
            year_dict.update(ids_dict)

        year_map[year] = int(len(year_dict))

        month_map[year] = {}
        day_map[year] = {}

        month_group_by = year_frame.groupby('month')

        for month, month_frame in month_group_by:
            month = int(month)
            month_dict = {}
            for ids_dict in month_frame['employee_record_ids'].values:
                month_dict.update(ids_dict)
            month_map[year][month] = len(month_dict)

            day_map[year][month] = {}

            day_group_by = month_frame.groupby('day')
            for day, day_frame in day_group_by:
                day = int(day)
                day_map[year][month][day] = int(day_frame['count_or_sum'].sum())

    return year_map, month_map, day_map


def get_total_office_count(date_range):
    offices_objs = ReportTotalOfficesModel.objects.filter(
        report_date__lte=date_range[1])
    office_count_dict = offices_objs.aggregate(Sum('count_or_sum'))
    office_count = office_count_dict['count_or_sum__sum']

    if not office_count:
        office_count = 0

    return office_count


def get_nispottikritto_nothi_count(date_range):
    nispottikritto_nothi_objects = ReportNispottikrittoNothiModel.objects.filter(
        report_day__range=date_range)
    nispottikritto_nothi_dict = nispottikritto_nothi_objects.aggregate(
        Sum('count_or_sum'))
    nispottikritto_nothi_count = nispottikritto_nothi_dict['count_or_sum__sum']

    if not nispottikritto_nothi_count:
        nispottikritto_nothi_count = 0

    return nispottikritto_nothi_count


def get_upokarvogi_count(date_range):
    upokarvogi_objects = ReportUpokarvogiModel.objects.filter(
        report_day__range=date_range)
    upokarvogi_dict = upokarvogi_objects.aggregate(Sum('count_or_sum'))
    upokarvogi = upokarvogi_dict['count_or_sum__sum']

    if not upokarvogi:
        upokarvogi = 0

    return upokarvogi


def get_potrojari_count(date_range):
    potrojari_objects = ReportPotrojariModel.objects.filter(
        report_day__range=date_range)
    potrojari_dict = potrojari_objects.aggregate(Sum('count_or_sum'))
    potrojari = potrojari_dict['count_or_sum__sum']

    if not potrojari:
        potrojari = 0

    return potrojari


def get_note_nisponno_count(date_range):
    note_nisponno_objects = ReportNoteNisponnoModel.objects.filter(
        report_day__range=date_range)
    note_nisponno_dict = note_nisponno_objects.aggregate(Sum('count_or_sum'))
    note_nisponno = note_nisponno_dict['count_or_sum__sum']

    if not note_nisponno:
        note_nisponno = 0

    return note_nisponno


def get_login_total_users(date_range):

    login_total_users_objects = ReportLoginTotalUsers.objects.filter(
        report_day__range=date_range)
    count_dict = {}
    for obj in login_total_users_objects:
        count_dict.update(obj.employee_record_ids)
    login_total_users = len(count_dict)
    if not login_total_users:
        login_total_users = 0

    return login_total_users

def get_total_login_count(date_range):

    querysets = ReportLoginTotalUsersNotDistinct.objects.filter(
        report_date__range=date_range)

    sum_dict = querysets.aggregate(Sum('counts'))
    counts = sum_dict['counts__sum']

    if not counts:
        counts = 0

    return counts


def get_login_male_users(date_range):
    login_male_users_objects = ReportLoginMalelUsersModel.objects.filter(
        report_day__range=date_range)
    count_dict = {}
    for obj in login_male_users_objects:
        count_dict.update(obj.employee_record_ids)
    login_male_users = len(count_dict)
    if not login_male_users:
        login_male_users = 0

    return login_male_users


def get_login_female_users(date_range):
    login_female_users_objects = ReportLoginFemalelUsersModel.objects.filter(
        report_day__range=date_range)
    count_dict = {}
    for obj in login_female_users_objects:
        count_dict.update(obj.employee_record_ids)
    login_female_users = len(count_dict)
    if not login_female_users:
        login_female_users = 0

    return login_female_users


def get_mobile_app_users(date_range):
    mobile_app_users_objects = ReportMobileAppUsersModel.objects.filter(
        report_day__range=date_range)

    count_dict = {}
    for obj in mobile_app_users_objects:
        count_dict.update(obj.employee_record_ids)
    mobile_app_users = len(count_dict)

    if not mobile_app_users:
        mobile_app_users = 0

    return mobile_app_users


def get_total_users(date_range):
    total_users_objs = ReportTotalUsersModel.objects.filter(
        report_day__lte=date_range[1])
    total_users_dict = total_users_objs.aggregate(Sum('count_or_sum'))
    total_users = total_users_dict['count_or_sum__sum']

    if not total_users:
        total_users = 0

    return total_users


def get_nothi_users_male(date_range):
    nothi_users_male_objs = ReportMaleNothiUsersModel.objects.filter(
        report_day__lte=date_range[1])
    nothi_users_male_dict = nothi_users_male_objs.aggregate(
        Sum('count_or_sum'))
    nothi_users_male = nothi_users_male_dict['count_or_sum__sum']

    if not nothi_users_male:
        nothi_users_male = 0

    return nothi_users_male


def get_nothi_users_female(date_range):
    nothi_users_female_objs = ReportFemaleNothiUsersModel.objects.filter(
        report_day__lte=date_range[1])
    nothi_users_female_dict = nothi_users_female_objs.aggregate(
        Sum('count_or_sum'))
    nothi_users_female = nothi_users_female_dict['count_or_sum__sum']

    if not nothi_users_female:
        nothi_users_female = 0

    return nothi_users_female
