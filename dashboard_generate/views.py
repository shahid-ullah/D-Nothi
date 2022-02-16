# dashboard_generate/views.py
import csv
import json
from datetime import datetime

import numpy as np
import pandas as pd
from django.db.models import Sum
from django.http import HttpResponse
# from django.http import FileResponse
from django.shortcuts import render

from .forms import ReportDateRangeForm
from .models import (ReportAndroidUsersModel, ReportFemaleNothiUsersModel,
                     ReportIOSUsersModel, ReportLoginFemalelUsersModel,
                     ReportLoginMalelUsersModel, ReportLoginTotalUsers,
                     ReportMaleNothiUsersModel, ReportMobileAppUsersModel,
                     ReportNispottikrittoNothiModel, ReportNoteNisponnoModel,
                     ReportPotrojariModel, ReportTotalOfficesModel,
                     ReportTotalUsersModel, ReportUpokarvogiModel)

# from monthly_report.views.views import mobile_app_users

CACHED_DICTIONARY = {}


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


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


# Create your views here.
def total_offices_view(request):
    global CACHED_DICTIONARY
    total_offices = CACHED_DICTIONARY.setdefault('total_offices', {})
    if total_offices:
        year_map = CACHED_DICTIONARY['total_offices']['year_map']
        month_map = CACHED_DICTIONARY['total_offices']['month_map']
        day_map = CACHED_DICTIONARY['total_offices']['day_map']
    else:
        objs = ReportTotalOfficesModel.objects.all()
        year_map, month_map, day_map = generate_year_month_and_day_map(objs)
        CACHED_DICTIONARY['total_offices']['year_map'] = year_map
        CACHED_DICTIONARY['total_offices']['month_map'] = month_map
        CACHED_DICTIONARY['total_offices']['day_map'] = day_map

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/total_offices.html', context)


nispottikritto_nothi_general_series = None
nispottikritto_nothi_drilldown_series = None


def nispottikritto_nothi_view(request):
    global CACHED_DICTIONARY
    nispottikritto_nothi = CACHED_DICTIONARY.setdefault('nispottikritto_nothi', {})
    if nispottikritto_nothi:
        year_map = CACHED_DICTIONARY['nispottikritto_nothi']['year_map']
        month_map = CACHED_DICTIONARY['nispottikritto_nothi']['month_map']
        day_map = CACHED_DICTIONARY['nispottikritto_nothi']['day_map']
    else:
        objs = ReportNispottikrittoNothiModel.objects.all()
        year_map, month_map, day_map = generate_year_month_and_day_map(objs)
        CACHED_DICTIONARY['nispottikritto_nothi']['year_map'] = year_map
        CACHED_DICTIONARY['nispottikritto_nothi']['month_map'] = month_map
        CACHED_DICTIONARY['nispottikritto_nothi']['day_map'] = day_map

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/nispottikritto_nothi.html', context)


def nothi_users_total(request):
    global CACHED_DICTIONARY
    nothi_users_total = CACHED_DICTIONARY.setdefault('nothi_users_total', {})
    if nothi_users_total:
        year_map = CACHED_DICTIONARY['nothi_users_total']['year_map']
        month_map = CACHED_DICTIONARY['nothi_users_total']['month_map']
        day_map = CACHED_DICTIONARY['nothi_users_total']['day_map']
    else:
        objs = ReportTotalUsersModel.objects.all()
        year_map, month_map, day_map = generate_year_month_and_day_map(objs)
        CACHED_DICTIONARY['nothi_users_total']['year_map'] = year_map
        CACHED_DICTIONARY['nothi_users_total']['month_map'] = month_map
        CACHED_DICTIONARY['nothi_users_total']['day_map'] = day_map
    # objs = ReportTotalUsersModel.objects.all()
    # year_map, month_map, day_map = generate_year_month_and_day_map(objs)
    # global nispottikritto_nothi_general_series, nispottikritto_nothi_drilldown_series
    # if nispottikritto_nothi_general_series and nispottikritto_nothi_drilldown_series:
    #     context = {
    #         'general_series': json.dumps(
    #             nispottikritto_nothi_general_series, cls=NpEncoder
    #         ),
    #         'drilldown_series': json.dumps(
    #             nispottikritto_nothi_drilldown_series, cls=NpEncoder
    #         ),
    #     }
    #     return render(request, 'monthly_report/nispottikritto_nothi.html', context)

    # general_series, drilldown_series = load_nispottikritto_nothi_graph_data()

    # nispottikritto_nothi_general_series = copy.deepcopy(general_series)
    # nispottikritto_nothi_drilldown_series = copy.deepcopy(drilldown_series)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/nothi_users_total.html', context)


def total_upokarvogi(request):
    global CACHED_DICTIONARY
    upokarvogi = CACHED_DICTIONARY.setdefault('upokarvogi', {})
    if upokarvogi:
        year_map = CACHED_DICTIONARY['upokarvogi']['year_map']
        month_map = CACHED_DICTIONARY['upokarvogi']['month_map']
        day_map = CACHED_DICTIONARY['upokarvogi']['day_map']
    else:
        objs = ReportUpokarvogiModel.objects.all()
        year_map, month_map, day_map = generate_year_month_and_day_map(objs)
        CACHED_DICTIONARY['upokarvogi']['year_map'] = year_map
        CACHED_DICTIONARY['upokarvogi']['month_map'] = month_map
        CACHED_DICTIONARY['upokarvogi']['day_map'] = day_map
    # objs = ReportUpokarvogiModel.objects.all()
    # year_map, month_map, day_map = generate_year_month_and_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/total_upokarvogi.html', context)


def nothi_users_male(request):
    global CACHED_DICTIONARY
    nothi_users_male_cache = CACHED_DICTIONARY.setdefault('nothi_users_male_cache', {})
    if nothi_users_male_cache:
        year_map = CACHED_DICTIONARY['nothi_users_male_cache']['year_map']
        month_map = CACHED_DICTIONARY['nothi_users_male_cache']['month_map']
        day_map = CACHED_DICTIONARY['nothi_users_male_cache']['day_map']
    else:
        objs = ReportMaleNothiUsersModel.objects.all()
        year_map, month_map, day_map = generate_year_month_and_day_map(objs)
        CACHED_DICTIONARY['nothi_users_male_cache']['year_map'] = year_map
        CACHED_DICTIONARY['nothi_users_male_cache']['month_map'] = month_map
        CACHED_DICTIONARY['nothi_users_male_cache']['day_map'] = day_map
    # objs = ReportMaleNothiUsersModel.objects.all()
    # year_map, month_map, day_map = generate_year_month_and_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/nothi_users_male.html', context)


def nothi_users_female(request):
    global CACHED_DICTIONARY
    nothi_users_female_cache = CACHED_DICTIONARY.setdefault(
        'nothi_users_female_cache', {}
    )
    if nothi_users_female_cache:
        year_map = CACHED_DICTIONARY['nothi_users_female_cache']['year_map']
        month_map = CACHED_DICTIONARY['nothi_users_female_cache']['month_map']
        day_map = CACHED_DICTIONARY['nothi_users_female_cache']['day_map']
    else:
        objs = ReportFemaleNothiUsersModel.objects.all()
        year_map, month_map, day_map = generate_year_month_and_day_map(objs)
        CACHED_DICTIONARY['nothi_users_female_cache']['year_map'] = year_map
        CACHED_DICTIONARY['nothi_users_female_cache']['month_map'] = month_map
        CACHED_DICTIONARY['nothi_users_female_cache']['day_map'] = day_map
    # objs = ReportFemaleNothiUsersModel.objects.all()
    # year_map, month_map, day_map = generate_year_month_and_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/nothi_users_female.html', context)


def note_nisponno(request):
    global CACHED_DICTIONARY
    note_nisponno_cache = CACHED_DICTIONARY.setdefault('note_nisponno_cache', {})
    if note_nisponno_cache:
        year_map = CACHED_DICTIONARY['note_nisponno_cache']['year_map']
        month_map = CACHED_DICTIONARY['note_nisponno_cache']['month_map']
        day_map = CACHED_DICTIONARY['note_nisponno_cache']['day_map']
    else:
        objs = ReportNoteNisponnoModel.objects.all()
        year_map, month_map, day_map = generate_year_month_and_day_map(objs)
        CACHED_DICTIONARY['note_nisponno_cache']['year_map'] = year_map
        CACHED_DICTIONARY['note_nisponno_cache']['month_map'] = month_map
        CACHED_DICTIONARY['note_nisponno_cache']['day_map'] = day_map
    # objs = ReportNoteNisponnoModel.objects.all()
    # year_map, month_map, day_map = generate_year_month_and_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/note_nisponno.html', context)


def potrojari_view(request):
    global CACHED_DICTIONARY
    potrojari_cache = CACHED_DICTIONARY.setdefault('potrojari_cache', {})
    if potrojari_cache:
        year_map = CACHED_DICTIONARY['potrojari_cache']['year_map']
        month_map = CACHED_DICTIONARY['potrojari_cache']['month_map']
        day_map = CACHED_DICTIONARY['potrojari_cache']['day_map']
    else:
        objs = ReportPotrojariModel.objects.all()
        year_map, month_map, day_map = generate_year_month_and_day_map(objs)
        CACHED_DICTIONARY['potrojari_cache']['year_map'] = year_map
        CACHED_DICTIONARY['potrojari_cache']['month_map'] = month_map
        CACHED_DICTIONARY['potrojari_cache']['day_map'] = day_map
    # objs = ReportPotrojariModel.objects.all()
    # year_map, month_map, day_map = generate_year_month_and_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/potrojari.html', context)


def generate_login_total_users_year_month_day_map(objs):
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


def login_total_users_view(request):
    global CACHED_DICTIONARY
    login_total_users = CACHED_DICTIONARY.setdefault('login_total_users', {})
    if login_total_users:
        year_map = CACHED_DICTIONARY['login_total_users']['year_map']
        month_map = CACHED_DICTIONARY['login_total_users']['month_map']
        day_map = CACHED_DICTIONARY['login_total_users']['day_map']
    else:
        objs = ReportLoginTotalUsers.objects.all()
        year_map, month_map, day_map = generate_year_month_and_day_map(objs)
        CACHED_DICTIONARY['login_total_users']['year_map'] = year_map
        CACHED_DICTIONARY['login_total_users']['month_map'] = month_map
        CACHED_DICTIONARY['login_total_users']['day_map'] = day_map
    # objs = ReportLoginTotalUsers.objects.all()
    # year_map, month_map, day_map = generate_login_total_users_year_month_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/login_total_users.html', context)


def login_male_users_view(request):
    global CACHED_DICTIONARY
    login_male_users_cache = CACHED_DICTIONARY.setdefault('login_male_users_cache', {})
    if login_male_users_cache:
        year_map = CACHED_DICTIONARY['login_male_users_cache']['year_map']
        month_map = CACHED_DICTIONARY['login_male_users_cache']['month_map']
        day_map = CACHED_DICTIONARY['login_male_users_cache']['day_map']
    else:
        objs = ReportLoginMalelUsersModel.objects.all()
        year_map, month_map, day_map = generate_year_month_and_day_map(objs)
        CACHED_DICTIONARY['login_male_users_cache']['year_map'] = year_map
        CACHED_DICTIONARY['login_male_users_cache']['month_map'] = month_map
        CACHED_DICTIONARY['login_male_users_cache']['day_map'] = day_map
    # objs = ReportLoginMalelUsersModel.objects.all()
    # year_map, month_map, day_map = generate_login_total_users_year_month_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/login_male_users.html', context)


def login_female_users_view(request):
    global CACHED_DICTIONARY
    login_female_users_cache = CACHED_DICTIONARY.setdefault(
        'login_female_users_cache', {}
    )
    if login_female_users_cache:
        year_map = CACHED_DICTIONARY['login_female_users_cache']['year_map']
        month_map = CACHED_DICTIONARY['login_female_users_cache']['month_map']
        day_map = CACHED_DICTIONARY['login_female_users_cache']['day_map']
    else:
        objs = ReportLoginFemalelUsersModel.objects.all()
        year_map, month_map, day_map = generate_year_month_and_day_map(objs)
        CACHED_DICTIONARY['login_female_users_cache']['year_map'] = year_map
        CACHED_DICTIONARY['login_female_users_cache']['month_map'] = month_map
        CACHED_DICTIONARY['login_female_users_cache']['day_map'] = day_map
    # objs = ReportLoginFemalelUsersModel.objects.all()
    # year_map, month_map, day_map = generate_login_total_users_year_month_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/login_female_users.html', context)


def mobile_app_users_view(request):

    global CACHED_DICTIONARY
    mobile_app_users_cache = CACHED_DICTIONARY.setdefault('mobile_app_users_cache', {})
    if mobile_app_users_cache:
        year_map = CACHED_DICTIONARY['mobile_app_users_cache']['year_map']
        month_map = CACHED_DICTIONARY['mobile_app_users_cache']['month_map']
        day_map = CACHED_DICTIONARY['mobile_app_users_cache']['day_map']
    else:
        objs = ReportMobileAppUsersModel.objects.all()
        year_map, month_map, day_map = generate_year_month_and_day_map(objs)
        CACHED_DICTIONARY['mobile_app_users_cache']['year_map'] = year_map
        CACHED_DICTIONARY['mobile_app_users_cache']['month_map'] = month_map
        CACHED_DICTIONARY['mobile_app_users_cache']['day_map'] = day_map
    # objs = ReportMobileAppUsersModel.objects.all()
    # year_map, month_map, day_map = generate_year_month_and_day_map(objs)
    android_users = ReportAndroidUsersModel.objects.aggregate(Sum('count_or_sum'))
    ios_users = ReportIOSUsersModel.objects.aggregate(Sum('count_or_sum'))

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
        'android_users': json.dumps(android_users['count_or_sum__sum'], cls=NpEncoder),
        'ios_users': json.dumps(ios_users['count_or_sum__sum'], cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/mobile_app_users.html', context)


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


def process_post_request(request):
    year_month_day = ''
    form = ReportDateRangeForm(request.POST)
    if form.is_valid():
        from_date = form.cleaned_data['From']
        to_date = form.cleaned_data['To']

        start_date = datetime(from_date.year, from_date.month, from_date.day)
        end_date = datetime(to_date.year, to_date.month, to_date.day)
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        date_range = [start_date, end_date]
        # total_offices
        office_count = get_total_office_count(date_range)
        # nispottikritto_nothi
        nispottikritto_nothi_count = get_nispottikritto_nothi_count(date_range)
        # upokarvogi
        upokarvogi = get_upokarvogi_count(date_range)
        # potrojari
        potrojari = get_potrojari_count(date_range)
        #  note nisponno
        note_nisponno = get_note_nisponno_count(date_range)
        # total users
        total_users = get_total_users(date_range)
        # nothi users male
        nothi_users_male = get_nothi_users_male(date_range)
        # nothi users female
        nothi_users_female = get_nothi_users_female(date_range)
        # mobile app users
        mobile_app_users = get_mobile_app_users(date_range)

        # login total users
        login_total_users = get_login_total_users(date_range)
        # login male users
        login_male_users = get_login_male_users(date_range)
        # login female users
        login_female_users = get_login_female_users(date_range)

        y1 = start_date.year
        y2 = end_date.year
        m1 = start_date.month
        m2 = end_date.month
        d1 = start_date.day
        d2 = end_date.day

        start_date = str(y1) + '-' + str(m1) + '-' + str(d1)
        end_date = str(y2) + '-' + str(m2) + '-' + str(d2)

        context = {
            'offices': {
                'total_offices': {
                    'count': office_count,
                    'date_from': '',
                    'date_to': year_month_day,
                }
            },
            'nisponno_records': {
                'nispottikritto_nothi': {
                    'count': nispottikritto_nothi_count,
                    'date_from': '',
                    'date_to': year_month_day,
                },
                'upokarvogi': {
                    'count': upokarvogi,
                    'date_from': '',
                    'date_to': year_month_day,
                },
                'potrojari': {
                    'count': potrojari,
                    'date_from': '',
                    'date_to': year_month_day,
                },
                'note_nisponno': {
                    'count': note_nisponno,
                    'date_from': '',
                    'date_to': year_month_day,
                },
            },
            'users': {
                'total_users': {
                    'count': total_users,
                    'date_from': '',
                    'date_to': year_month_day,
                }
            },
            'users_employee_records': {
                'nothi_users_male': {
                    'count': nothi_users_male,
                    'date_from': '',
                    'date_to': year_month_day,
                },
                'nothi_users_female': {
                    'count': nothi_users_female,
                    'date_from': '',
                    'date_to': year_month_day,
                },
            },
            'user_login_history': {
                'mobile_app_users': {
                    'count': mobile_app_users,
                    'date_range': '12/12/20',
                },
                # 'android_ios_users': {'count': office_count, 'date_range': '12/12/20'},
            },
            'login_history_employee_records': {
                'login_total_users': {
                    'count': login_total_users,
                    'date_range': '12/12/20',
                },
                'login_male_users': {
                    'count': login_male_users,
                    'date_range': '12/12/20',
                },
                'login_female_users': {
                    'count': login_female_users,
                    'date_range': '12/12/20',
                },
            },
            'form': form,
            'start_date': start_date,
            'end_date': end_date,
        }

        return render(
            request, 'dashboard_generate/custom_report.html', context={'data': context}
        )
    else:
        return HttpResponse('Date format not correct')


def custom_report(request):
    if request.method == 'POST':
        return process_post_request(request)

    form = ReportDateRangeForm()
    context = {}
    from datetime import date

    today = date.today()

    year = today.year
    month = today.month
    day = today.day
    year_month_day = str(day) + "/" + str(month) + "/" + str(year)

    office_count_dict = ReportTotalOfficesModel.objects.aggregate(Sum('count_or_sum'))
    office_count = office_count_dict['count_or_sum__sum']

    # nispottikritto_nothi
    nispottikritto_nothi_objects = ReportNispottikrittoNothiModel.objects.filter(
        year=year, month=month
    )
    nispottikritto_nothi_dict = nispottikritto_nothi_objects.aggregate(
        Sum('count_or_sum')
    )
    nispottikritto_nothi_count = nispottikritto_nothi_dict['count_or_sum__sum']
    if not nispottikritto_nothi_count:
        nispottikritto_nothi_count = 0

    # upokarvogi
    upokarvogi_objects = ReportUpokarvogiModel.objects.filter(year=year, month=month)
    upokarvogi_dict = upokarvogi_objects.aggregate(Sum('count_or_sum'))
    upokarvogi = upokarvogi_dict['count_or_sum__sum']
    if not upokarvogi:
        upokarvogi = 0

    # potrojari
    potrojari_objects = ReportPotrojariModel.objects.filter(year=year, month=month)
    potrojari_dict = potrojari_objects.aggregate(Sum('count_or_sum'))
    potrojari = potrojari_dict['count_or_sum__sum']
    if not potrojari:
        potrojari = 0

    # note nisponno
    note_nisponno_objects = ReportNoteNisponnoModel.objects.filter(
        year=year, month=month
    )
    note_nisponno_dict = note_nisponno_objects.aggregate(Sum('count_or_sum'))
    note_nisponno = note_nisponno_dict['count_or_sum__sum']
    if not note_nisponno:
        note_nisponno = 0

    total_users_dict = ReportTotalUsersModel.objects.aggregate(Sum('count_or_sum'))
    total_users = total_users_dict['count_or_sum__sum']

    # nothi users male
    nothi_users_male_dict = ReportMaleNothiUsersModel.objects.aggregate(
        Sum('count_or_sum')
    )
    nothi_users_male = nothi_users_male_dict['count_or_sum__sum']

    # nothi users female
    nothi_users_female_dict = ReportFemaleNothiUsersModel.objects.aggregate(
        Sum('count_or_sum')
    )
    nothi_users_female = nothi_users_female_dict['count_or_sum__sum']

    # mobile app users
    mobile_app_users_objects = ReportMobileAppUsersModel.objects.filter(
        year=year, month=month
    )
    mobile_app_users_dict = mobile_app_users_objects.aggregate(Sum('count_or_sum'))
    mobile_app_users = mobile_app_users_dict['count_or_sum__sum']
    if not mobile_app_users:
        mobile_app_users = 0

    # total users (login)
    login_total_users_objects = ReportLoginTotalUsers.objects.filter(
        year=year, month=month
    )
    login_total_users_dict = login_total_users_objects.aggregate(Sum('count_or_sum'))
    login_total_users = login_total_users_dict['count_or_sum__sum']
    if not login_total_users:
        login_total_users = 0

    # total nothi users (male login)
    login_male_users_objects = ReportLoginMalelUsersModel.objects.filter(
        year=year, month=month
    )
    login_male_users_dict = login_male_users_objects.aggregate(Sum('count_or_sum'))
    login_male_users = login_male_users_dict['count_or_sum__sum']
    if not login_male_users:
        login_male_users = 0

    # total nothi users (female login)
    login_female_users_objects = ReportLoginFemalelUsersModel.objects.filter(
        year=year, month=month
    )
    login_female_users_dict = login_female_users_objects.aggregate(Sum('count_or_sum'))
    login_female_users = login_female_users_dict['count_or_sum__sum']
    if not login_female_users:
        login_female_users = 0

    context = {
        'offices': {
            'total_offices': {
                'count': office_count,
                'date_from': '',
                'date_to': year_month_day,
            }
        },
        'nisponno_records': {
            'nispottikritto_nothi': {
                'count': nispottikritto_nothi_count,
                'date_from': '',
                'date_to': year_month_day,
            },
            'upokarvogi': {
                'count': upokarvogi,
                'date_from': '',
                'date_to': year_month_day,
            },
            'potrojari': {
                'count': potrojari,
                'date_from': '',
                'date_to': year_month_day,
            },
            'note_nisponno': {
                'count': note_nisponno,
                'date_from': '',
                'date_to': year_month_day,
            },
        },
        'users': {
            'total_users': {
                'count': total_users,
                'date_from': '',
                'date_to': year_month_day,
            }
        },
        'users_employee_records': {
            'nothi_users_male': {
                'count': nothi_users_male,
                'date_from': '',
                'date_to': year_month_day,
            },
            'nothi_users_female': {
                'count': nothi_users_female,
                'date_from': '',
                'date_to': year_month_day,
            },
        },
        'user_login_history': {
            'mobile_app_users': {'count': mobile_app_users, 'date_range': '12/12/20'},
            # 'android_ios_users': {'count': office_count, 'date_range': '12/12/20'},
        },
        'login_history_employee_records': {
            'login_total_users': {'count': login_total_users, 'date_range': '12/12/20'},
            'login_male_users': {'count': login_male_users, 'date_range': '12/12/20'},
            'login_female_users': {
                'count': login_female_users,
                'date_range': '12/12/20',
            },
        },
        'form': form,
        'start_date': str(year) + '-' + str(month) + '-' + str(day),
        'end_date': str(year) + '-' + str(month) + '-' + str(day),
    }

    return render(
        request,
        'dashboard_generate/custom_report.html',
        context={
            'data': context,
        },
    )


def report_export_csv(request, start_date=None, end_date=None):
    start_date = start_date.split('-')
    end_date = end_date.split('-')
    start_date = datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    end_date = datetime(int(end_date[0]), int(end_date[1]), int(end_date[2]))
    date_range = [start_date, end_date]
    office_count = get_total_office_count(date_range)
    # nispottikritto_nothi
    nispottikritto_nothi_count = get_nispottikritto_nothi_count(date_range)
    # upokarvogi
    upokarvogi = get_upokarvogi_count(date_range)
    # potrojari
    potrojari = get_potrojari_count(date_range)
    #  note nisponno
    note_nisponno = get_note_nisponno_count(date_range)
    # total users
    total_users = get_total_users(date_range)
    # nothi users male
    nothi_users_male = get_nothi_users_male(date_range)
    # nothi users female
    nothi_users_female = get_nothi_users_female(date_range)

    # mobile app users
    mobile_app_users = get_mobile_app_users(date_range)

    # login total users
    login_total_users = get_login_total_users(date_range)
    # login male users
    login_male_users = get_login_male_users(date_range)
    # login female users
    login_female_users = get_login_female_users(date_range)

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['    সূচক   ', '      সংখ্যা      '])
    writer.writerow(['মোট অফিস', office_count])
    writer.writerow(['নিস্পত্তিকৃত নথি', nispottikritto_nothi_count])

    writer.writerow(['মোট উপকারভোগী', upokarvogi])
    writer.writerow(['নোট নিষ্পন্ন', note_nisponno])
    writer.writerow(['পত্রজারি', potrojari])
    writer.writerow(['মোট ব্যবহারকারী', total_users])
    writer.writerow(['মোট নথি ব্যবহারকারী (পুরুষ)', nothi_users_male])
    writer.writerow(['মোট নথি ব্যবহারকারী (মহিলা)', nothi_users_female])
    writer.writerow(['মোট ব্যবহারকারী (লগইন)', login_total_users])
    writer.writerow(['মোট নথি ব্যবহারকারী (পুরুষ লগইন)', login_male_users])
    writer.writerow(['মোট নথি ব্যবহারকারী (মহিলা লগইন)', login_female_users])
    writer.writerow(['মোবাইল অ্যাপ ব্যবহারকারী', mobile_app_users])
    now = datetime.now()
    filename = now.strftime("%Y%m%d%H%M%S")
    filename = 'report_' + filename + '.csv'
    content_disposition = f'attachment; filename={filename}'
    response['Content-Disposition'] = content_disposition

    return response
