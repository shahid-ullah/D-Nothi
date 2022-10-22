from django.db.models import Sum

from automate_process.scripts.reports import login_total_users

from ..models import (
    ReportFemaleNothiUsersModel,
    ReportLoginFemalelUsersModel,
    ReportLoginMalelUsersModel,
    ReportLoginTotalUsers,
    ReportMaleNothiUsersModel,
    ReportMobileAppUsersModel,
    ReportNispottikrittoNothiModel,
    ReportNoteNisponnoModel,
    ReportPotrojariModel,
    ReportTotalOfficesModel,
    ReportTotalUsersModel,
    ReportUpokarvogiModel,
)


def get_report():

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
        nothi_users_male_dict = ReportMaleNothiUsersModel.objects.aggregate(Sum('count_or_sum'))
        male_users_total = int(nothi_users_male_dict['count_or_sum__sum'])

        if not male_users_total:
            male_users_total = 0
    except Exception as _:
        male_users_total = 0

    # female users total calculate
    try:
        nothi_users_female_dict = ReportFemaleNothiUsersModel.objects.aggregate(Sum('count_or_sum'))
        female_users_total = int(nothi_users_female_dict['count_or_sum__sum'])

        if not female_users_total:
            female_users_total = 0
    except Exception as _:
        female_users_total = 0

    # calculate login users total
    try:
        login_total_users_objects = ReportLoginTotalUsers.objects.all()
        count_dict = {}
        for obj in login_total_users_objects:
            count_dict.update(obj.employee_record_ids)
        login_users_total = len(count_dict)
    except Exception as _:
        login_users_total = 0

    # login male users total calculate
    try:
        login_male_users_objects = ReportLoginMalelUsersModel.objects.all()
        count_dict = {}
        for obj in login_male_users_objects:
            count_dict.update(obj.employee_record_ids)
        login_male_users_total = len(count_dict)
    except Exception as _:
        login_male_users_total = 0

    # login female users total calculate
    try:
        login_female_users_objects = ReportLoginFemalelUsersModel.objects.all()
        count_dict = {}
        for obj in login_female_users_objects:
            count_dict.update(obj.employee_record_ids)
        female_login_users_total = len(count_dict)
    except Exception as _:
        female_login_users_total = 0

    # nispottikritto_nothi total calculate for current month
    try:
        nispottikritto_nothi_objects = ReportNispottikrittoNothiModel.objects.all()
        nispottikritto_nothi_dict = nispottikritto_nothi_objects.aggregate(Sum('count_or_sum'))
        nispottikritto_nothi_count = int(nispottikritto_nothi_dict['count_or_sum__sum'])
        if not nispottikritto_nothi_count:
            nispottikritto_nothi_count = 0
    except Exception as _:
        nispottikritto_nothi_count = 0

    # upokarvogi total calculate for current month
    try:
        upokarvogi_objects = ReportUpokarvogiModel.objects.all()
        upokarvogi_dict = upokarvogi_objects.aggregate(Sum('count_or_sum'))
        upokarvogi = int(upokarvogi_dict['count_or_sum__sum'])
        if not upokarvogi:
            upokarvogi = 0
    except Exception as _:
        upokarvogi = 0

    # potrojari total calculate for current month
    try:
        potrojari_objects = ReportPotrojariModel.objects.all()
        potrojari_dict = potrojari_objects.aggregate(Sum('count_or_sum'))
        potrojari = int(potrojari_dict['count_or_sum__sum'])
        if not potrojari:
            potrojari = 0
    except Exception as _:
        potrojari = 0

    # note nisponno total calculate for current month
    try:
        note_nisponno_objects = ReportNoteNisponnoModel.objects.all()
        note_nisponno_dict = note_nisponno_objects.aggregate(Sum('count_or_sum'))
        note_nisponno = int(note_nisponno_dict['count_or_sum__sum'])
        if not note_nisponno:
            note_nisponno = 0
    except Exception as _:
        note_nisponno = 0

    # mobile app users total calculate for current month
    try:
        mobile_app_users_objects = ReportMobileAppUsersModel.objects.all()
        mobile_app_users_dict = mobile_app_users_objects.aggregate(Sum('count_or_sum'))
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
