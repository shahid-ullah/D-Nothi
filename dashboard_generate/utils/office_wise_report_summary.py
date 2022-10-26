from datetime import datetime

import pandas as pd
from django.db.models import Sum

from dashboard_generate.models import (
    ReportLoginFemalelUsersModel,
    ReportLoginMalelUsersModel,
    ReportLoginTotalUsers,
    ReportLoginTotalUsersNotDistinct,
    ReportMobileAppUsersModel,
    ReportNispottikrittoNothiModel,
    ReportNoteNisponnoModel,
    ReportPotrojariModel,
    ReportUpokarvogiModel,
)


def office_ids_string_to_list(office_ids_string):
    office_ids = []
    if office_ids_string:
        office_ids_string = office_ids_string.strip(', ')
        office_id_list = office_ids_string.split(',')
        for office_id in office_id_list:
            try:
                office_ids.append(int(office_id))
            except Exception as e:
                print(e)

    return office_ids


def get_login_total(date_range, office_ids):

    office_ids_counts = {}
    querysets = ReportLoginTotalUsersNotDistinct.objects.all()
    querysets = querysets.filter(report_date__range=date_range, office_id__in=office_ids)

    if querysets:
        dataframe = pd.DataFrame(querysets.values('office_id', 'counts'))
        grouped = dataframe.groupby('office_id', sort=False, as_index=False)['counts'].sum()
        office_ids_counts = {office_id: counts for office_id, counts in zip(grouped['office_id'], grouped['counts'])}

    return office_ids_counts


def get_login_total_users(date_range, office_ids):

    office_ids_counts = {}
    querysets = ReportLoginTotalUsers.objects.all()
    querysets = querysets.filter(report_date__range=date_range, office_id__in=office_ids)

    if querysets:
        dataframe = pd.DataFrame(querysets.values('office_id', 'employee_record_ids'))
        grouped = dataframe.groupby('office_id', sort=False, as_index=False)
        for group, frame in grouped:
            unique_employee_record_ids = {}
            for employee_record_ids in frame['employee_record_ids'].values:
                unique_employee_record_ids.update(employee_record_ids)

            office_ids_counts[group] = len(unique_employee_record_ids)

    return office_ids_counts


def get_login_total_male_users(date_range, office_ids):

    office_ids_counts = {}
    querysets = ReportLoginMalelUsersModel.objects.all()
    querysets = querysets.filter(report_date__range=date_range, office_id__in=office_ids)

    if querysets:
        dataframe = pd.DataFrame(querysets.values('office_id', 'employee_record_ids'))
        grouped = dataframe.groupby('office_id', sort=False, as_index=False)
        for group, frame in grouped:
            unique_employee_record_ids = {}
            for employee_record_ids in frame['employee_record_ids'].values:
                unique_employee_record_ids.update(employee_record_ids)

            office_ids_counts[group] = len(unique_employee_record_ids)

    return office_ids_counts


def get_login_total_female_users(date_range, office_ids):

    office_ids_counts = {}
    querysets = ReportLoginFemalelUsersModel.objects.all()
    querysets = querysets.filter(report_date__range=date_range, office_id__in=office_ids)

    if querysets:
        dataframe = pd.DataFrame(querysets.values('office_id', 'employee_record_ids'))
        grouped = dataframe.groupby('office_id', sort=False, as_index=False)
        for group, frame in grouped:
            unique_employee_record_ids = {}
            for employee_record_ids in frame['employee_record_ids'].values:
                unique_employee_record_ids.update(employee_record_ids)

            office_ids_counts[group] = len(unique_employee_record_ids)

    return office_ids_counts


def get_office_wise_report_summary(office_ids_string='', from_date='', to_date=''):
    office_ids = office_ids_string_to_list(office_ids_string)

    if not to_date:
        today = datetime.today()
        to_date = datetime(today.year, today.month, today.day)
    else:
        to_date = to_date.split('-')
        to_date = datetime(int(to_date[2]), int(to_date[1]), int(to_date[0]))

    from_date = from_date.split('-')
    from_date = datetime(int(from_date[2]), int(from_date[1]), int(from_date[0]))

    if from_date > to_date:
        from_date, to_date = to_date, from_date

    date_range = [from_date, to_date]

    login_total = get_login_total(date_range, office_ids)
    login_total_users = get_login_total_users(date_range, office_ids)
    login_total_male_users = get_login_total_male_users(date_range, office_ids)
    login_total_female_users = get_login_total_female_users(date_range, office_ids)

    context = {
        'reports': {
            'login_total': login_total,
            'login_total_users': login_total_users,
            'login_total_male_users': login_total_male_users,
            'login_total_female_users': login_total_female_users,
        },
        'office_ids': office_ids,
    }

    return context
