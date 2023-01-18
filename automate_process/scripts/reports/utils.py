# automate_process/scripts/reports/utils.py
from datetime import timedelta

from automate_process.models import (
    EmployeeRecords,
    NisponnoRecords,
    Offices,
    SourceDBLog,
    TrackSourceDBLastFetchTime,
    UserLoginHistory,
    Users,
)
from backup_source_db.models import BackupDBLog, TrackBackupDBLastFetchTime
from dashboard_generate.models import (
    ReportLoginTotalUsers,
    ReportNispottikrittoNothiModel,
    ReportTotalOfficesModel,
    ReportTotalUsersModel,
)


def get_offices_querysets(*args, **kwargs):
    last_fetch_time_object = TrackBackupDBLastFetchTime.objects.using('backup_source_db').last()
    querysets = Offices.objects.using('source_db').all()
    try:
        last_fetch_time = last_fetch_time_object.offices
        querysets = querysets.filter(created__gt=last_fetch_time)
    except AttributeError:
        last_fetch_time = ReportTotalOfficesModel.objects.last().report_date
        last_fetch_time = last_fetch_time + timedelta(days=1)
        querysets = querysets.filter(created__gt=last_fetch_time)

    return querysets


def get_user_login_history_querysets(*args, **kwargs):
    last_fetch_time_object = TrackBackupDBLastFetchTime.objects.using('backup_source_db').last()
    # querysets = UserLoginHistory.objects.using('source_db').all()
    querysets = UserLoginHistory.objects.using('source_db').filter(id__lt=100000)
    # try:
    #     last_fetch_time = last_fetch_time_object.user_login_history
    #     querysets = querysets.filter(created__gt=last_fetch_time)
    # except AttributeError:
    #     last_fetch_time = ReportLoginTotalUsers.objects.last().report_day
    #     last_fetch_time = last_fetch_time + timedelta(days=1)
    #     querysets = querysets.filter(created__gt=last_fetch_time)

    return querysets


def get_nisponno_records_querysets(*args, **kwargs):
    last_fetch_time_object = TrackBackupDBLastFetchTime.objects.using('backup_source_db').last()
    querysets = NisponnoRecords.objects.using('source_db').all()
    try:
        last_fetch_time = last_fetch_time_object.nisponno_records
        querysets = querysets.filter(created__gt=last_fetch_time)
    except AttributeError:
        last_fetch_time = ReportNispottikrittoNothiModel.objects.last().report_day
        last_fetch_time = last_fetch_time + timedelta(days=1)
        querysets = querysets.filter(created__gt=last_fetch_time)

    return querysets


def get_users_querysets(*args, **kwargs):
    last_fetch_time_object = TrackBackupDBLastFetchTime.objects.using('backup_source_db').last()
    querysets = Users.objects.using('source_db').all()
    try:
        last_fetch_time = last_fetch_time_object.users
        querysets = querysets.filter(created__gt=last_fetch_time)
    except AttributeError:
        last_fetch_time = ReportTotalUsersModel.objects.last().report_day
        last_fetch_time = last_fetch_time + timedelta(days=1)
        querysets = querysets.filter(created__gt=last_fetch_time)

    return querysets


def get_employee_records_querysets(*args, **kwargs):
    # we always need full employee records
    querysets = EmployeeRecords.objects.using('source_db').all()
    # try:
    #     last_fetch_time = last_fetch_time_object.users
    #     querysets = querysets.filter(created__gt=last_fetch_time)
    # except AttributeError:
    #     last_fetch_time = ReportTotalUsersModel.objects.last().report_day
    #     querysets = querysets.filter(created__gt=last_fetch_time)

    return querysets


def update_backup_db_last_fetch_time(request, *args, **kwargs):
    print()
    print('updating backup DB last_fetch_time')
    time_object = TrackSourceDBLastFetchTime.objects.using('source_db').first()
    object_dict = {}
    object_dict['offices'] = time_object.offices
    object_dict['employee_records'] = time_object.employee_records
    object_dict['nisponno_records'] = time_object.nisponno_records
    object_dict['user_login_history'] = time_object.user_login_history
    TrackBackupDBLastFetchTime.objects.using('backup_source_db').create(**object_dict)
    print('End updating backup DB last_fetch_time')
    print()

    return None


def update_backup_db_log(request, *args, **kwargs):
    last_log_map = kwargs['last_log_map']
    print()
    print('updating backup DB log')
    # log_object = SourceDBLog.objects.using('source_db').last()
    # object_dict = {}
    # object_dict['last_office_id'] = log_object.last_office_id
    # object_dict['last_user_id'] = log_object.last_user_id
    # object_dict['last_employee_id'] = log_object.last_employee_id
    # object_dict['last_nisponno_records_time'] = log_object.last_nisponno_records_time
    # object_dict['last_login_history_time'] = log_object.last_login_history_time
    # BackupDBLog.objects.using('backup_source_db').create(**object_dict)
    BackupDBLog.objects.using('backup_source_db').create(**last_log_map)
    print('End updating backup DB log')
    print()

    return None
