# dashboard_generate/views.py
# import copy
# import io
import json

import numpy as np
import pandas as pd
from django.db.models import Sum
# from django.http import FileResponse
from django.shortcuts import render

from .models import (ReportFemaleNothiUsersModel, ReportMaleNothiUsersModel,
                     ReportNispottikrittoNothiModel, ReportNoteNisponnoModel,
                     ReportPotrojariModel, ReportTotalOfficesModel,
                     ReportTotalUsersModel, ReportUpokarvogiModel)

# from datetime import datetime


# from reportlab.pdfgen import canvas
# from rest_framework import views
# from rest_framework.response import Response


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
    objs = ReportTotalOfficesModel.objects.all()
    year_map, month_map, day_map = generate_year_month_and_day_map(objs)
    # breakpoint()

    # global offices_general_series, offices_'drilldown'_series
    # if offices_general_series and offices_'drilldown'_series:
    #     context = {
    #         'general_series': json.dumps(offices_general_series, cls=NpEncoder),
    #         ''drilldown'_series': json.dumps(offices_'drilldown'_series, cls=NpEncoder),
    #     }
    #     return render(request, 'monthly_report/dashboard.html', context)

    # general_series, 'drilldown'_series = load_total_offices_graph_data()

    # offices_general_series = copy.deepcopy(general_series)
    # offices_'drilldown'_series = copy.deepcopy('drilldown'_series)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/total_offices.html', context)


nispottikritto_nothi_general_series = None
nispottikritto_nothi_drilldown_series = None


def nispottikritto_nothi_view(request):
    objs = ReportNispottikrittoNothiModel.objects.all()
    year_map, month_map, day_map = generate_year_month_and_day_map(objs)
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

    return render(request, 'dashboard_generate/nispottikritto_nothi.html', context)


def nothi_users_total(request):
    objs = ReportTotalUsersModel.objects.all()
    year_map, month_map, day_map = generate_year_month_and_day_map(objs)
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
    objs = ReportUpokarvogiModel.objects.all()
    year_map, month_map, day_map = generate_year_month_and_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/total_upokarvogi.html', context)


def nothi_users_male(request):
    objs = ReportMaleNothiUsersModel.objects.all()
    year_map, month_map, day_map = generate_year_month_and_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/nothi_users_male.html', context)


def nothi_users_female(request):
    objs = ReportFemaleNothiUsersModel.objects.all()
    year_map, month_map, day_map = generate_year_month_and_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/nothi_users_female.html', context)


def note_nisponno(request):
    objs = ReportNoteNisponnoModel.objects.all()
    year_map, month_map, day_map = generate_year_month_and_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/note_nisponno.html', context)


def potrojari_view(request):
    objs = ReportPotrojariModel.objects.all()
    year_map, month_map, day_map = generate_year_month_and_day_map(objs)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/potrojari.html', context)


def custom_report(request):
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

    nothi_users_male_dict = ReportMaleNothiUsersModel.objects.aggregate(
        Sum('count_or_sum')
    )
    nothi_users_male = nothi_users_male_dict['count_or_sum__sum']

    nothi_users_female_dict = ReportFemaleNothiUsersModel.objects.aggregate(
        Sum('count_or_sum')
    )
    nothi_users_female = nothi_users_female_dict['count_or_sum__sum']
    # breakpoint()

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
        # 'user_login_history': {
        #     'mobile_app_users': {'count': office_count, 'date_range': '12/12/20'},
        #     'android_ios_users': {'count': office_count, 'date_range': '12/12/20'},
        # },
    }

    return render(request, 'dashboard_generate/custom_report.html', context)
