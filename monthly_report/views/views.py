# filename: src/clinic/views.py

import copy
import json

from django.conf import settings
from django.shortcuts import render

from ..utils import (NpEncoder, generate_general_series_drilldown_series,
                     load_mobile_users_dataframe,
                     load_nisponno_records_dataframe, load_office_dataframe,
                     load_potrojari_dataframe, load_total_nisponno_dataframe,
                     load_users_dataframe, load_users_gender_female_dataframe,
                     load_users_gender_male_dataframe)


def dashboard(request):
    dataframe = load_office_dataframe()

    office_count = dataframe.groupby('year').size()
    office_numbers = list(office_count.values)
    office_years = list(office_count.index.values)

    context = {
        "office_years": json.dumps(office_years, cls=NpEncoder),
        "office_numbers": json.dumps(office_numbers, cls=NpEncoder),
    }

    return render(request, 'monthly_report/dashboard.html', context)


def nispottikritto_nothi_yearwise(request):
    load_nisponno_records_dataframe()
    nisponno_records_df = settings.NISPONNO_RECORDS_CSV_FILE_PATH
    nisponno_records_count = nisponno_records_df.groupby('year').size()
    records_numbers = list(nisponno_records_count.values)
    records_years = list(nisponno_records_count.index.values)
    context = {
        'record_numbers': json.dumps(records_numbers, cls=NpEncoder),
        'record_years': json.dumps(records_years, cls=NpEncoder),
    }
    return render(request, 'monthly_report/nispottikritto_nothi_yearwise.html', context)


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

    dataframe = load_nisponno_records_dataframe()
    dataframe_year_by = dataframe.groupby('year')
    general_series, drilldown_series = generate_general_series_drilldown_series(
        dataframe_year_by, 'offices'
    )
    nispottikritto_nothi_general_series = copy.deepcopy(general_series)
    nispottikritto_nothi_drilldown_series = copy.deepcopy(drilldown_series)

    context = {
        'general_series': json.dumps(
            nispottikritto_nothi_general_series, cls=NpEncoder
        ),
        'drilldown_series': json.dumps(
            nispottikritto_nothi_drilldown_series, cls=NpEncoder
        ),
    }

    dataframe = None
    dataframe_year_by = None
    general_series = None
    drilldown_series = None

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

    dataframe = load_users_dataframe()
    dataframe_year_by = dataframe.groupby('year')

    general_series, drilldown_series = generate_general_series_drilldown_series(
        dataframe_year_by, 'users'
    )

    nothi_users_total_general_series = copy.deepcopy(general_series)
    nothi_users_total_drilldown_series = copy.deepcopy(drilldown_series)

    context = {
        'general_series': json.dumps(nothi_users_total_general_series, cls=NpEncoder),
        'drilldown_series': json.dumps(
            nothi_users_total_drilldown_series, cls=NpEncoder
        ),
    }

    dataframe = None
    dataframe_year_by = None
    general_series = None
    drilldown_series = None

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

    dataframe = load_users_gender_male_dataframe()
    dataframe_year_by = dataframe.groupby('year')
    general_series, drilldown_series = generate_general_series_drilldown_series(
        dataframe_year_by, 'users'
    )

    male_users_general_series = copy.deepcopy(general_series)
    male_users_drilldown_series = copy.deepcopy(drilldown_series)

    dataframe = None
    dataframe_year_by = None
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

    dataframe = load_users_gender_female_dataframe()
    dataframe_year_by = dataframe.groupby('year')
    general_series, drilldown_series = generate_general_series_drilldown_series(
        dataframe_year_by, 'users'
    )
    female_users_general_series = copy.deepcopy(general_series)
    female_users_drilldown_series = copy.deepcopy(drilldown_series)

    dataframe = None
    dataframe_year_by = None
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

    if mobile_users_general_series and mobile_users_drilldown_series:
        context = {
            'general_series': json.dumps(mobile_users_general_series, cls=NpEncoder),
            'drilldown_series': json.dumps(
                mobile_users_drilldown_series, cls=NpEncoder
            ),
        }
        return render(request, 'monthly_report/mobile_app_users.html', context)

    dataframe = load_mobile_users_dataframe()
    dataframe_year_by = dataframe.groupby('year')

    general_series, drilldown_series = generate_general_series_drilldown_series(
        dataframe_year_by, 'users'
    )
    mobile_users_general_series = copy.deepcopy(general_series)
    mobile_users_drilldown_series = copy.deepcopy(drilldown_series)

    dataframe = None
    dataframe_year_by = None
    general_series = None
    drilldown_series = None

    context = {
        'general_series': json.dumps(mobile_users_general_series, cls=NpEncoder),
        'drilldown_series': json.dumps(mobile_users_drilldown_series, cls=NpEncoder),
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

    dataframe = load_total_nisponno_dataframe()
    dataframe_year_by = dataframe.groupby('year')

    general_series, drilldown_series = generate_general_series_drilldown_series(
        dataframe_year_by, 'years'
    )
    total_nisponno_general_series = copy.deepcopy(general_series)
    total_nisponno_drilldown_series = copy.deepcopy(drilldown_series)

    dataframe = None
    dataframe_year_by = None
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

    dataframe = load_potrojari_dataframe()
    dataframe_year_by = dataframe.groupby('year')

    general_series, drilldown_series = generate_general_series_drilldown_series(
        dataframe_year_by, 'years'
    )
    potrojari_general_series = copy.deepcopy(general_series)
    potrojari_drilldown_series = copy.deepcopy(drilldown_series)

    dataframe = None
    dataframe_year_by = None
    general_series = None
    drilldown_series = None

    context = {
        'general_series': json.dumps(potrojari_general_series, cls=NpEncoder),
        'drilldown_series': json.dumps(potrojari_drilldown_series, cls=NpEncoder),
    }

    return render(request, 'monthly_report/potrojari.html', context)
