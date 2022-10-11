from datetime import datetime

from django.db.models import Sum

from .models import (
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


def get_mobile_app_users(date_range, office_ids):
    mobile_app_users_objects = ReportMobileAppUsersModel.objects.filter(report_day__range=date_range)

    count_dict = {}
    for obj in mobile_app_users_objects:
        count_dict.update(obj.employee_record_ids)
    mobile_app_users = len(count_dict)

    if not mobile_app_users:
        mobile_app_users = 0

    return mobile_app_users


def get_note_nisponno_count(date_range, office_ids):
    querysets = ReportNoteNisponnoModel.objects.all()

    if office_ids:
        querysets = querysets.filter(report_day__range=date_range, office_id__in=office_ids)
    else:
        querysets = querysets.filter(report_day__range=date_range)

    note_nisponno_dict = querysets.aggregate(Sum('count_or_sum'))
    note_nisponno = note_nisponno_dict['count_or_sum__sum']

    if not note_nisponno:
        note_nisponno = 0

    return note_nisponno


def get_potrojari_count(date_range, office_ids):
    querysets = ReportPotrojariModel.objects.all()

    if office_ids:
        querysets = querysets.filter(report_day__range=date_range, office_id__in=office_ids)
    else:
        querysets = querysets.filter(report_day__range=date_range)

    potrojari_dict = querysets.aggregate(Sum('count_or_sum'))
    potrojari = potrojari_dict['count_or_sum__sum']

    if not potrojari:
        potrojari = 0

    return potrojari


def get_upokarvogi_count(date_range, office_ids):
    querysets = ReportUpokarvogiModel.objects.all()

    if office_ids:
        querysets = querysets.filter(report_day__range=date_range, office_id__in=office_ids)
    else:
        querysets = querysets.filter(report_day__range=date_range)

    upokarvogi_dict = querysets.aggregate(Sum('count_or_sum'))
    upokarvogi = upokarvogi_dict['count_or_sum__sum']

    if not upokarvogi:
        upokarvogi = 0

    return upokarvogi


def get_nispottikritto_nothi_count(date_range, office_ids):

    querysets = ReportNispottikrittoNothiModel.objects.all()

    if office_ids:
        querysets = querysets.filter(report_day__range=date_range, office_id__in=office_ids)
    else:
        querysets = querysets.filter(report_day__range=date_range)

    nispottikritto_nothi_dict = querysets.aggregate(Sum('count_or_sum'))
    nispottikritto_nothi_count = nispottikritto_nothi_dict['count_or_sum__sum']

    if not nispottikritto_nothi_count:
        nispottikritto_nothi_count = 0

    return nispottikritto_nothi_count


def get_total_login_count(date_range, office_ids):

    querysets = ReportLoginTotalUsersNotDistinct.objects.all()

    if office_ids:
        querysets = querysets.filter(report_date__range=date_range, office_id__in=office_ids)
    else:
        querysets = querysets.filter(report_date__range=date_range)

    sum_dict = querysets.aggregate(Sum('counts'))
    counts = sum_dict['counts__sum']

    if not counts:
        counts = 0

    return counts


def get_report_summary(office_ids_string='', from_date='', to_date=''):
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

    # nispottikritto_nothi
    nispottikritto_nothi_count = get_nispottikritto_nothi_count(date_range, office_ids)
    # upokarvogi
    upokarvogi = get_upokarvogi_count(date_range, office_ids)
    # potrojari
    potrojari = get_potrojari_count(date_range, office_ids)
    # note nisponno
    note_nisponno = get_note_nisponno_count(date_range, office_ids)
    # login total users not distinct
    total_login = get_total_login_count(date_range, office_ids)

    context = {
        'reports': {
            'nispottikritto_nothi': nispottikritto_nothi_count,
            'upokarvogi': upokarvogi,
            'potrojari': potrojari,
            'note_nisponno': note_nisponno,
            'total_login': total_login,
        },
        'office_ids': office_ids,
    }

    return context
