# dashboard_generate/veiws.py
import csv
import json
from datetime import date, datetime

import pandas as pd
from django.contrib.auth import get_user_model

# from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# from . import graph_methods
from . import helper_functions
from .forms import ReportDateRangeForm
from .models import (
    ReportAndroidUsersModel,
    ReportFemaleNothiUsersModel,
    ReportIOSUsersModel,
    ReportLoginFemalelUsersModel,
    ReportLoginMalelUsersModel,
    ReportLoginTotalUsers,
    ReportLoginTotalUsersNotDistinct,
    ReportMaleNothiUsersModel,
    ReportMobileAppUsersModel,
    ReportNispottikrittoNothiModel,
    ReportNoteNisponnoModel,
    ReportPotrojariModel,
    ReportTotalOfficesModel,
    ReportTotalUsersModel,
    ReportUpokarvogiModel,
)
from .report_summary import get_report_summary
from .utils import total_report_summary_count
from .utils.dnothi_office_wise_report_summary import get_dnothi_office_wise_report_summary
from .utils.office_wise_report_summary import get_office_wise_report_summary

User = get_user_model()

MAP_MONTH_BENGLI_NAME = {
    '1': 'জানুয়ারি',
    '2': 'ফেব্রুয়ারী',
    '3': 'মার্চ',
    '4': 'এপ্রিল',
    '5': 'মে',
    '6': 'জুন',
    '7': 'জুলাই',
    '8': 'আগস্ট',
    '9': 'সেপ্টেম্বর',
    '10': 'অক্টোবর',
    '11': 'নভেম্বর',
    '12': 'ডিসেম্বর',
}


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def dashboard_home(request):
    today = datetime.now()

    month = MAP_MONTH_BENGLI_NAME[str(today.month)]
    year = today.year

    if is_ajax(request=request):
        stack_bar_chart = helper_functions.generate_login_stack_bar_chart_data()
        return JsonResponse(stack_bar_chart)

    # General report summary count
    report_summary_count = helper_functions.get_report_summary_count()
    total_report_summary_count_ = total_report_summary_count.get_report()

    # Plot note_nisponno data
    plot_note_nisponno_data = {}

    try:
        year_map, month_map, day_map = helper_functions.get_cache_or_calculate(
            'note_nisponno', helper_functions.generate_year_month_and_day_map, ReportNoteNisponnoModel
        )
        plot_note_nisponno_data['year_map'] = year_map
        plot_note_nisponno_data['month_map'] = month_map
        plot_note_nisponno_data['day_map'] = day_map
    except Exception as _:
        plot_note_nisponno_data['year_map'] = {}
        plot_note_nisponno_data['month_map'] = {}
        plot_note_nisponno_data['day_map'] = {}

    # plot login stack bar data
    # stack_bar_chart = helper_functions.generate_login_stack_bar_chart_data()
    stack_bar_chart = [{}]

    # plot nispottikritto nothi data
    nispottikritto_nothi_plot = helper_functions.generate_nispottikritto_nothi_plot_data()

    data = {
        'report_summary_count': report_summary_count,
        'total_report_summary_count': total_report_summary_count_,
        'stack_bar_chart': stack_bar_chart,
        'nispottikritto_nothi_plot': nispottikritto_nothi_plot,
        'plot_note_nisponno_data': plot_note_nisponno_data,
        'month': month,
        'year': year,
    }

    return render(request, 'dashboard_ui/index.html', context={'data': data})


# @login_required(login_url='/sso_login_handler/')
def total_offices_view(request):
    year_map, month_map, day_map = helper_functions.get_cache_or_calculate(
        'total_offices', helper_functions.generate_year_month_and_day_map, ReportTotalOfficesModel
    )

    context = {
        'year_map': json.dumps(year_map, cls=helper_functions.NpEncoder),
        'month_map': json.dumps(month_map, cls=helper_functions.NpEncoder),
        'day_map': json.dumps(day_map, cls=helper_functions.NpEncoder),
    }

    return render(request, 'dashboard_generate/total_offices.html', context)


def ministry_wise_total_login_view(request):
    objs = ReportLoginTotalUsersNotDistinct.objects.all()
    ministry_map = {}
    context = {}

    if objs.exists():
        report_start_date = objs.first().report_date
        report_end_date = objs.last().report_date
        values = objs.values()
        df = pd.DataFrame(values)
        grouped = df.groupby(['ministry_id'], sort=False, as_index=False)['counts'].sum()
        grouped = grouped.astype({'ministry_id': str})

        ministry_map = dict(zip(grouped['ministry_id'].values, grouped['counts'].values))

        context = {
            'ministry_map': json.dumps(ministry_map, cls=helper_functions.NpEncoder),
            'report_start_date': report_start_date,
            'report_end_date': report_end_date,
        }

    return render(request, 'dashboard_generate/ministry_wise_total_login.html', context)


# @login_required(login_url='/sso_login_handler/')
def nispottikritto_nothi_view(request):
    year_map, month_map, day_map = helper_functions.get_cache_or_calculate(
        'nispottikritto_nothi',
        helper_functions.generate_year_month_and_day_map,
        ReportNispottikrittoNothiModel,
    )

    context = {
        'year_map': json.dumps(year_map, cls=helper_functions.NpEncoder),
        'month_map': json.dumps(month_map, cls=helper_functions.NpEncoder),
        'day_map': json.dumps(day_map, cls=helper_functions.NpEncoder),
    }

    return render(request, 'dashboard_generate/nispottikritto_nothi.html', context)


# @login_required(login_url='/sso_login_handler/')
def nothi_users_total_view(request):
    year_map, month_map, day_map = helper_functions.get_cache_or_calculate(
        'nothi_users_total', helper_functions.generate_year_month_and_day_map, ReportTotalUsersModel
    )

    context = {
        'year_map': json.dumps(year_map, cls=helper_functions.NpEncoder),
        'month_map': json.dumps(month_map, cls=helper_functions.NpEncoder),
        'day_map': json.dumps(day_map, cls=helper_functions.NpEncoder),
    }

    return render(request, 'dashboard_generate/nothi_users_total.html', context)


# @login_required(login_url='/sso_login_handler/')
def total_upokarvogi_view(request):
    year_map, month_map, day_map = helper_functions.get_cache_or_calculate(
        'upokarvogi', helper_functions.generate_year_month_and_day_map, ReportUpokarvogiModel
    )

    context = {
        'year_map': json.dumps(year_map, cls=helper_functions.NpEncoder),
        'month_map': json.dumps(month_map, cls=helper_functions.NpEncoder),
        'day_map': json.dumps(day_map, cls=helper_functions.NpEncoder),
    }

    return render(request, 'dashboard_generate/total_upokarvogi.html', context)


# @login_required(login_url='/sso_login_handler/')
def nothi_users_male_view(request):
    year_map, month_map, day_map = helper_functions.get_cache_or_calculate(
        'nothi_users_male',
        helper_functions.generate_year_month_and_day_map,
        ReportMaleNothiUsersModel,
    )

    context = {
        'year_map': json.dumps(year_map, cls=helper_functions.NpEncoder),
        'month_map': json.dumps(month_map, cls=helper_functions.NpEncoder),
        'day_map': json.dumps(day_map, cls=helper_functions.NpEncoder),
    }

    return render(request, 'dashboard_generate/nothi_users_male.html', context)


# @login_required(login_url='/sso_login_handler/')
def nothi_users_female_view(request):
    year_map, month_map, day_map = helper_functions.get_cache_or_calculate(
        'nothi_users_female',
        helper_functions.generate_year_month_and_day_map,
        ReportFemaleNothiUsersModel,
    )

    context = {
        'year_map': json.dumps(year_map, cls=helper_functions.NpEncoder),
        'month_map': json.dumps(month_map, cls=helper_functions.NpEncoder),
        'day_map': json.dumps(day_map, cls=helper_functions.NpEncoder),
    }

    return render(request, 'dashboard_generate/nothi_users_female.html', context)


# @login_required(login_url='/sso_login_handler/')
def note_nisponno_view(request):
    year_map, month_map, day_map = helper_functions.get_cache_or_calculate(
        'note_nisponno', helper_functions.generate_year_month_and_day_map, ReportNoteNisponnoModel
    )

    context = {
        'year_map': json.dumps(year_map, cls=helper_functions.NpEncoder),
        'month_map': json.dumps(month_map, cls=helper_functions.NpEncoder),
        'day_map': json.dumps(day_map, cls=helper_functions.NpEncoder),
    }

    return render(request, 'dashboard_generate/note_nisponno.html', context)


# @login_required(login_url='/sso_login_handler/')
def potrojari_view(request):
    year_map, month_map, day_map = helper_functions.get_cache_or_calculate(
        'potrojari', helper_functions.generate_year_month_and_day_map, ReportPotrojariModel
    )

    context = {
        'year_map': json.dumps(year_map, cls=helper_functions.NpEncoder),
        'month_map': json.dumps(month_map, cls=helper_functions.NpEncoder),
        'day_map': json.dumps(day_map, cls=helper_functions.NpEncoder),
    }

    return render(request, 'dashboard_generate/potrojari.html', context)


# @login_required(login_url='/sso_login_handler/')
def login_total_users_view(request):
    querysets = ReportLoginTotalUsers.objects.all()
    year_map, month_map, day_map = helper_functions.generate_login_users_year_month_day_map(querysets)

    context = {
        'year_map': json.dumps(year_map, cls=helper_functions.NpEncoder),
        'month_map': json.dumps(month_map, cls=helper_functions.NpEncoder),
        'day_map': json.dumps(day_map, cls=helper_functions.NpEncoder),
    }

    return render(request, 'dashboard_generate/login_total_users.html', context)


# @login_required(login_url='/sso_login_handler/')
def login_male_users_view(request):
    year_map, month_map, day_map = helper_functions.get_cache_or_calculate(
        'login_male_users',
        helper_functions.generate_login_users_year_month_day_map,
        ReportLoginMalelUsersModel,
    )

    context = {
        'year_map': json.dumps(year_map, cls=helper_functions.NpEncoder),
        'month_map': json.dumps(month_map, cls=helper_functions.NpEncoder),
        'day_map': json.dumps(day_map, cls=helper_functions.NpEncoder),
    }

    return render(request, 'dashboard_generate/login_male_users.html', context)


# @login_required(login_url='/sso_login_handler/')
def login_female_users_view(request):
    year_map, month_map, day_map = helper_functions.get_cache_or_calculate(
        'login_female_users',
        helper_functions.generate_login_users_year_month_day_map,
        ReportLoginFemalelUsersModel,
    )

    context = {
        'year_map': json.dumps(year_map, cls=helper_functions.NpEncoder),
        'month_map': json.dumps(month_map, cls=helper_functions.NpEncoder),
        'day_map': json.dumps(day_map, cls=helper_functions.NpEncoder),
    }

    return render(request, 'dashboard_generate/login_female_users.html', context)


# @login_required(login_url='/sso_login_handler/')
def mobile_app_users_view(request):
    year_map, month_map, day_map = helper_functions.get_cache_or_calculate(
        'mobile_app_users',
        helper_functions.generate_login_users_year_month_day_map,
        ReportMobileAppUsersModel,
    )

    android_users = ReportAndroidUsersModel.objects.aggregate(Sum('count_or_sum'))
    ios_users = ReportIOSUsersModel.objects.aggregate(Sum('count_or_sum'))

    context = {
        'year_map': json.dumps(year_map, cls=helper_functions.NpEncoder),
        'month_map': json.dumps(month_map, cls=helper_functions.NpEncoder),
        'day_map': json.dumps(day_map, cls=helper_functions.NpEncoder),
        'android_users': json.dumps(android_users['count_or_sum__sum'], cls=helper_functions.NpEncoder),
        'ios_users': json.dumps(ios_users['count_or_sum__sum'], cls=helper_functions.NpEncoder),
    }

    return render(request, 'dashboard_generate/mobile_app_users.html', context)


def process_post_request(request):
    year_month_day = ''
    form = ReportDateRangeForm(request.POST)
    if form.is_valid():
        from_date = form.cleaned_data['From']
        to_date = form.cleaned_data['To']
        # breakpoint()
        start_date = datetime(from_date.year, from_date.month, from_date.day)
        end_date = datetime(to_date.year, to_date.month, to_date.day)
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        date_range = [start_date, end_date]
        # total_offices
        office_count = helper_functions.get_total_office_count(date_range)
        # nispottikritto_nothi
        nispottikritto_nothi_count = helper_functions.get_nispottikritto_nothi_count(date_range)
        # upokarvogi
        upokarvogi = helper_functions.get_upokarvogi_count(date_range)
        # potrojari
        potrojari = helper_functions.get_potrojari_count(date_range)
        #  note nisponno
        note_nisponno = helper_functions.get_note_nisponno_count(date_range)
        # total users
        total_users = helper_functions.get_total_users(date_range)
        # nothi users male
        nothi_users_male = helper_functions.get_nothi_users_male(date_range)
        # nothi users female
        nothi_users_female = helper_functions.get_nothi_users_female(date_range)
        # mobile app users
        mobile_app_users = helper_functions.get_mobile_app_users(date_range)

        # login total users
        login_total_users = helper_functions.get_login_total_users(date_range)
        # breakpoint()
        # total login counts (not distinct)
        total_login = helper_functions.get_total_login_count(date_range)
        # login male users
        login_male_users = helper_functions.get_login_male_users(date_range)
        # login female users
        login_female_users = helper_functions.get_login_female_users(date_range)

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
                'total_login': {
                    'count': total_login,
                    'date_range': '12/12/20',
                },
            },
            'form': form,
            'start_date': start_date,
            'end_date': end_date,
        }

        return render(request, 'dashboard_generate/custom_report.html', context={'data': context})
    else:
        return HttpResponse('Date format not correct')


# @login_required(login_url='/sso_login_handler/')
def custom_report(request):
    if request.method == 'POST':
        return process_post_request(request)

    form = ReportDateRangeForm()
    context = {}

    today = date.today()

    year = today.year
    month = today.month
    day = today.day
    year_month_day = str(day) + "/" + str(month) + "/" + str(year)

    office_count_dict = ReportTotalOfficesModel.objects.aggregate(Sum('count_or_sum'))
    office_count = office_count_dict['count_or_sum__sum']

    # nispottikritto_nothi
    nispottikritto_nothi_objects = ReportNispottikrittoNothiModel.objects.filter(year=year, month=month)
    nispottikritto_nothi_dict = nispottikritto_nothi_objects.aggregate(Sum('count_or_sum'))
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
    note_nisponno_objects = ReportNoteNisponnoModel.objects.filter(year=year, month=month)
    note_nisponno_dict = note_nisponno_objects.aggregate(Sum('count_or_sum'))
    note_nisponno = note_nisponno_dict['count_or_sum__sum']
    if not note_nisponno:
        note_nisponno = 0

    total_users_dict = ReportTotalUsersModel.objects.aggregate(Sum('count_or_sum'))
    total_users = total_users_dict['count_or_sum__sum']

    # nothi users male
    nothi_users_male_dict = ReportMaleNothiUsersModel.objects.aggregate(Sum('count_or_sum'))
    nothi_users_male = nothi_users_male_dict['count_or_sum__sum']

    # nothi users female
    nothi_users_female_dict = ReportFemaleNothiUsersModel.objects.aggregate(Sum('count_or_sum'))
    nothi_users_female = nothi_users_female_dict['count_or_sum__sum']

    # mobile app users
    mobile_app_users_objects = ReportMobileAppUsersModel.objects.filter(year=year, month=month)
    mobile_app_users_dict = mobile_app_users_objects.aggregate(Sum('count_or_sum'))
    mobile_app_users = mobile_app_users_dict['count_or_sum__sum']
    if not mobile_app_users:
        mobile_app_users = 0

    # total users (login)
    # login_total_users_distinct
    login_total_users_objects = ReportLoginTotalUsers.objects.filter(year=year, month=month)
    count_dict = {}
    for obj in login_total_users_objects:
        count_dict.update(obj.employee_record_ids)
    login_total_users = len(count_dict)

    # login_total_users_not_distinct
    # total login (not distinct count)
    total_login_objects = ReportLoginTotalUsersNotDistinct.objects.filter(year=year, month=month)
    total_login_dict = total_login_objects.aggregate(Sum('counts'))
    total_login = total_login_dict['counts__sum']
    if not total_login:
        total_login = 0

    # total nothi users (male login)
    login_male_users_objects = ReportLoginMalelUsersModel.objects.filter(year=year, month=month)
    count_dict = {}
    for obj in login_male_users_objects:
        count_dict.update(obj.employee_record_ids)
    login_male_users = len(count_dict)

    # total nothi users (female login)
    login_female_users_objects = ReportLoginFemalelUsersModel.objects.filter(year=year, month=month)
    count_dict = {}
    for obj in login_female_users_objects:
        count_dict.update(obj.employee_record_ids)
    login_female_users = len(count_dict)

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
            'total_login': {
                'count': total_login,
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


# @login_required(login_url='/sso_login_handler/')
def report_export_csv_view(request, start_date=None, end_date=None):
    start_date = start_date.split('-')
    end_date = end_date.split('-')
    start_date = datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    end_date = datetime(int(end_date[0]), int(end_date[1]), int(end_date[2]))
    date_range = [start_date, end_date]
    office_count = helper_functions.get_total_office_count(date_range)
    # nispottikritto_nothi
    nispottikritto_nothi_count = helper_functions.get_nispottikritto_nothi_count(date_range)
    # upokarvogi
    upokarvogi = helper_functions.get_upokarvogi_count(date_range)
    # potrojari
    potrojari = helper_functions.get_potrojari_count(date_range)
    #  note nisponno
    note_nisponno = helper_functions.get_note_nisponno_count(date_range)
    # total users
    total_users = helper_functions.get_total_users(date_range)
    # nothi users male
    nothi_users_male = helper_functions.get_nothi_users_male(date_range)
    # nothi users female
    nothi_users_female = helper_functions.get_nothi_users_female(date_range)

    # mobile app users
    mobile_app_users = helper_functions.get_mobile_app_users(date_range)

    # login total users
    login_total_users = helper_functions.get_login_total_users(date_range)

    # total login counts (not distinct)
    total_login = helper_functions.get_total_login_count(date_range)
    # login male users
    # login male users
    login_male_users = helper_functions.get_login_male_users(date_range)
    # login female users
    login_female_users = helper_functions.get_login_female_users(date_range)

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
    writer.writerow(['মোট লগইন', total_login])
    writer.writerow(['মোট নথি ব্যবহারকারী (পুরুষ লগইন)', login_male_users])
    writer.writerow(['মোট নথি ব্যবহারকারী (মহিলা লগইন)', login_female_users])
    writer.writerow(['মোবাইল অ্যাপ ব্যবহারকারী', mobile_app_users])
    now = datetime.now()
    filename = now.strftime("%Y%m%d%H%M%S")
    filename = 'report_' + filename + '.csv'
    content_disposition = f'attachment; filename={filename}'
    response['Content-Disposition'] = content_disposition

    return response


def report_summary(request):
    if is_ajax(request):
        office_ids = request.GET['office_ids']
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        response = get_report_summary(office_ids_string=office_ids, from_date=from_date, to_date=to_date)
        return JsonResponse(response)

    return render(request, 'dashboard_generate/report_summary.html', context={})


def office_wise_report_summary(request):
    if is_ajax(request):
        office_ids = request.GET['office_ids']
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        response = get_office_wise_report_summary(office_ids_string=office_ids, from_date=from_date, to_date=to_date)
        return JsonResponse(response)

    return render(request, 'dashboard_generate/office_wise_report_summary.html', context={})


def dnothi_office_wise_report_summary(request):
    if is_ajax(request):
        office_ids = request.GET['office_ids']
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        response = get_dnothi_office_wise_report_summary(
            office_ids_string=office_ids, from_date=from_date, to_date=to_date
        )
        return JsonResponse(response)

    return render(request, 'dashboard_generate/dnothi_office_wise_report_summary.html', context={})
