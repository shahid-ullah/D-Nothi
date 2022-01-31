# filename: src/clinic/views.py

import copy
import json

from django.shortcuts import render

from ..models import ReportStorageModel, TableNameModel
from ..utils import (NpEncoder, generate_general_series_and_drilldown_series,
                     load_mobile_app_users_graph_data,
                     load_nispottikritto_nothi_graph_data,
                     load_nothi_users_total_graph_data,
                     load_potrojari_graph_data, load_report_storage_table,
                     load_total_nisponno_graph_data,
                     load_total_offices_graph_data, load_upokarvogi_graph_data,
                     load_users_gender_female_graph_data,
                     load_users_gender_male_graph_data)

offices_general_series = None
offices_drilldown_series = None


def dashboard(request):
    global offices_general_series, offices_drilldown_series
    if offices_general_series and offices_drilldown_series:
        context = {
            'general_series': json.dumps(offices_general_series, cls=NpEncoder),
            'drilldown_series': json.dumps(offices_drilldown_series, cls=NpEncoder),
        }
        return render(request, 'monthly_report/dashboard.html', context)

    general_series, drilldown_series = load_total_offices_graph_data()

    offices_general_series = copy.deepcopy(general_series)
    offices_drilldown_series = copy.deepcopy(drilldown_series)

    general_series = None
    drilldown_series = None

    context = {
        'general_series': json.dumps(offices_general_series, cls=NpEncoder),
        'drilldown_series': json.dumps(offices_drilldown_series, cls=NpEncoder),
    }

    return render(request, 'monthly_report/dashboard.html', context)


# def nispottikritto_nothi_yearwise(request):
#     load_nisponno_records_dataframe()
#     nisponno_records_df = settings.NISPONNO_RECORDS_CSV_FILE_PATH
#     nisponno_records_count = nisponno_records_df.groupby('year').size()
#     records_numbers = list(nisponno_records_count.values)
#     records_years = list(nisponno_records_count.index.values)
#     context = {
#         'record_numbers': json.dumps(records_numbers, cls=NpEncoder),
#         'record_years': json.dumps(records_years, cls=NpEncoder),
#     }
#     return render(request, 'monthly_report/nispottikritto_nothi_yearwise.html', context)


nispottikritto_nothi_general_series = None
nispottikritto_nothi_drilldown_series = None


def nispottikritto_nothi(request):
    global nispottikritto_nothi_general_series, nispottikritto_nothi_drilldown_series
    if nispottikritto_nothi_general_series and nispottikritto_nothi_drilldown_series:
        context = {
            'general_series': json.dumps(
                nispottikritto_nothi_general_series, cls=NpEncoder
            ),
            'drilldown_series': json.dumps(
                nispottikritto_nothi_drilldown_series, cls=NpEncoder
            ),
        }
        return render(request, 'monthly_report/nispottikritto_nothi.html', context)

    general_series, drilldown_series = load_nispottikritto_nothi_graph_data()

    nispottikritto_nothi_general_series = copy.deepcopy(general_series)
    nispottikritto_nothi_drilldown_series = copy.deepcopy(drilldown_series)

    general_series = None
    drilldown_series = None

    context = {
        'general_series': json.dumps(
            nispottikritto_nothi_general_series, cls=NpEncoder
        ),
        'drilldown_series': json.dumps(
            nispottikritto_nothi_drilldown_series, cls=NpEncoder
        ),
    }

    return render(request, 'monthly_report/nispottikritto_nothi.html', context)


nothi_users_total_general_series = None
nothi_users_total_drilldown_series = None


def nothi_users_total(request):
    global nothi_users_total_general_series, nothi_users_total_drilldown_series
    if nothi_users_total_general_series and nothi_users_total_drilldown_series:
        context = {
            'general_series': json.dumps(
                nothi_users_total_general_series, cls=NpEncoder
            ),
            'drilldown_series': json.dumps(
                nothi_users_total_drilldown_series, cls=NpEncoder
            ),
        }
        return render(request, 'monthly_report/nothi_users_total.html', context)

    general_series, drilldown_series = load_nothi_users_total_graph_data()

    nothi_users_total_general_series = copy.deepcopy(general_series)
    nothi_users_total_drilldown_series = copy.deepcopy(drilldown_series)

    general_series = None
    drilldown_series = None

    context = {
        'general_series': json.dumps(nothi_users_total_general_series, cls=NpEncoder),
        'drilldown_series': json.dumps(
            nothi_users_total_drilldown_series, cls=NpEncoder
        ),
    }

    return render(request, 'monthly_report/nothi_users_total.html', context)


male_users_general_series = None
male_users_drilldown_series = None


def nothi_users_male(request):
    global male_users_general_series, male_users_drilldown_series
    if male_users_general_series and male_users_drilldown_series:
        context = {
            'general_series': json.dumps(male_users_general_series, cls=NpEncoder),
            'drilldown_series': json.dumps(male_users_drilldown_series, cls=NpEncoder),
        }
        return render(request, 'monthly_report/nothi_users_male.html', context)

    general_series, drilldown_series = load_users_gender_male_graph_data()

    male_users_general_series = copy.deepcopy(general_series)
    male_users_drilldown_series = copy.deepcopy(drilldown_series)

    general_series = None
    drilldown_series = None

    context = {
        'general_series': json.dumps(male_users_general_series, cls=NpEncoder),
        'drilldown_series': json.dumps(male_users_drilldown_series, cls=NpEncoder),
    }

    return render(request, 'monthly_report/nothi_users_male.html', context)


female_users_general_series = None
female_users_drilldown_series = None


def nothi_users_female(request):
    global female_users_general_series, female_users_drilldown_series
    if female_users_general_series and female_users_drilldown_series:
        context = {
            'general_series': json.dumps(female_users_general_series, cls=NpEncoder),
            'drilldown_series': json.dumps(
                female_users_drilldown_series, cls=NpEncoder
            ),
        }
        return render(request, 'monthly_report/nothi_users_female.html', context)

    general_series, drilldown_series = load_users_gender_female_graph_data()

    female_users_general_series = copy.deepcopy(general_series)
    female_users_drilldown_series = copy.deepcopy(drilldown_series)

    general_series = None
    drilldown_series = None

    context = {
        'general_series': json.dumps(female_users_general_series, cls=NpEncoder),
        'drilldown_series': json.dumps(female_users_drilldown_series, cls=NpEncoder),
    }

    return render(request, 'monthly_report/nothi_users_female.html', context)


mobile_users_general_series = None
mobile_users_drilldown_series = None


def mobile_app_users(request):
    global mobile_users_general_series, mobile_users_drilldown_series

    # if mobile_users_general_series and mobile_users_drilldown_series:
    #     context = {
    #         'general_series': json.dumps(mobile_users_general_series, cls=NpEncoder),
    #         'drilldown_series': json.dumps(
    #             mobile_users_drilldown_series, cls=NpEncoder
    #         ),
    #     }
    #     return render(request, 'monthly_report/mobile_app_users.html', context)

    table_object = load_table_name_object(name='user_login_history')
    report_object = load_report_storage_model_object(table_name=table_object)
    data = load_json_data(report_object)

    mobile_app_users = data['mobile_app_users']
    general_series, drilldown_series = generate_general_series_and_drilldown_series(
        mobile_app_users, 'years'
    )
    android_ios_users = data['android_ios_users']

    mobile_users_general_series = copy.deepcopy(general_series)
    mobile_users_drilldown_series = copy.deepcopy(drilldown_series)

    general_series = None
    drilldown_series = None

    total = 0
    for dict_ in android_ios_users:

        for category, value in dict_.items():
            total = total + int(value)

    android_ios_users_percentage = []
    for dict_ in android_ios_users:
        dic = {}

        for category, value in dict_.items():
            dic[category] = int(round((int(value) * 100.0) / total))
            android_ios_users_percentage.append(dic)

    context = {
        'general_series': json.dumps(mobile_users_general_series, cls=NpEncoder),
        'drilldown_series': json.dumps(mobile_users_drilldown_series, cls=NpEncoder),
        'android_ios_users': json.dumps(android_ios_users_percentage, cls=NpEncoder),
    }

    return render(request, 'monthly_report/mobile_app_users.html', context)


total_nisponno_general_series = None
total_nisponno_drilldown_series = None


def total_nisponno(request):
    global total_nisponno_general_series, total_nisponno_drilldown_series

    if total_nisponno_general_series and total_nisponno_drilldown_series:
        context = {
            'general_series': json.dumps(total_nisponno_general_series, cls=NpEncoder),
            'drilldown_series': json.dumps(
                total_nisponno_drilldown_series, cls=NpEncoder
            ),
        }
        return render(request, 'monthly_report/total_nisponno.html', context)

    general_series, drilldown_series = load_total_nisponno_graph_data()

    total_nisponno_general_series = copy.deepcopy(general_series)
    total_nisponno_drilldown_series = copy.deepcopy(drilldown_series)

    general_series = None
    drilldown_series = None

    context = {
        'general_series': json.dumps(total_nisponno_general_series, cls=NpEncoder),
        'drilldown_series': json.dumps(total_nisponno_drilldown_series, cls=NpEncoder),
    }

    return render(request, 'monthly_report/total_nisponno.html', context)


potrojari_general_series = None
potrojari_drilldown_series = None


def potrojari(request):
    global potrojari_general_series, potrojari_drilldown_series

    if potrojari_general_series and potrojari_drilldown_series:
        context = {
            'general_series': json.dumps(potrojari_general_series, cls=NpEncoder),
            'drilldown_series': json.dumps(potrojari_drilldown_series, cls=NpEncoder),
        }
        return render(request, 'monthly_report/potrojari.html', context)

    general_series, drilldown_series = load_potrojari_graph_data()

    potrojari_general_series = copy.deepcopy(general_series)
    potrojari_drilldown_series = copy.deepcopy(drilldown_series)

    general_series = None
    drilldown_series = None

    context = {
        'general_series': json.dumps(potrojari_general_series, cls=NpEncoder),
        'drilldown_series': json.dumps(potrojari_drilldown_series, cls=NpEncoder),
    }

    return render(request, 'monthly_report/potrojari.html', context)


total_upokarvogi_general_series = None
total_upokarvogi_drilldown_series = None


def total_upokarvogi(request):
    global total_upokarvogi_general_series, total_upokarvogi_drilldown_series

    if total_upokarvogi_general_series and total_upokarvogi_drilldown_series:
        context = {
            'general_series': json.dumps(
                total_upokarvogi_general_series, cls=NpEncoder
            ),
            'drilldown_series': json.dumps(
                total_upokarvogi_drilldown_series, cls=NpEncoder
            ),
        }
        return render(request, 'monthly_report/total_upokarvogi.html', context)

    general_series, drilldown_series = load_upokarvogi_graph_data()

    total_upokarvogi_general_series = copy.deepcopy(general_series)
    total_upokarvogi_drilldown_series = copy.deepcopy(drilldown_series)

    general_series = None
    drilldown_series = None

    context = {
        'general_series': json.dumps(total_upokarvogi_general_series, cls=NpEncoder),
        'drilldown_series': json.dumps(
            total_upokarvogi_drilldown_series, cls=NpEncoder
        ),
    }

    return render(request, 'monthly_report/total_upokarvogi.html', context)


def load_table_user_login_history():
    table_obj = TableNameModel.objects.filter(name='user_login_history').last()
    report_storage_obj = ReportStorageModel.objects.filter(table_name=table_obj).last()

    with open(report_storage_obj.file_name.path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    return data


def load_table_name_object(name):
    table_object = TableNameModel.objects.filter(name=name).last()

    return table_object


def load_report_storage_model_object(table_name):
    report_object = ReportStorageModel.objects.filter(table_name=table_name).last()

    return report_object


def load_json_data(file_obj):
    with open(file_obj.file_name.path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    return data
