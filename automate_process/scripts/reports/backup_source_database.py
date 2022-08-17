from datetime import timedelta

from django.core.paginator import Paginator

from automate_process.models import (EmployeeRecords, NisponnoRecords, Offices,
                                     TrackSourceDBLastFetchTime,
                                     UserLoginHistory, Users)
from backup_source_db.models import (BackupEmployeeRecords,
                                     BackupNisponnoRecords, BackupOffices,
                                     BackupUserLoginHistory, BackupUsers)
from dashboard_generate.models import (ReportLoginTotalUsers,
                                       ReportNispottikrittoNothiModel)

print('Loading backup_source_db scripts')

CURRENT_DATABASE_FETCH_TIME = {}

# Backup Offices Table
def backup_office_table():
    last_fetched_date_object = TrackSourceDBLastFetchTime.objects.using('source_db').last()
    print('backup offices table ...')
    last_fetch_time = None

    querysets = Offices.objects.using('source_db').all()
    last_object = BackupOffices.objects.using('backup_source_db').last()

    # check office last fetch time from TrackSourceDBLastFetchTime Model
    # first time this will be absent.
    try:
        last_fetch_time = last_fetched_date_object.offices
    except AttributeError:
        pass

    # if last fetch time absent again check from BackupOffices Model
    # first backup time this will be absent.
    if not last_fetch_time:
        try:
            last_fetch_time = last_object.created
        except AttributeError:
            pass

    # first time backup this will be empty.
    # so we will backup whole table.
    if last_fetch_time:
        querysets = querysets.filter(created__gt=last_fetch_time)

    querysets = querysets.exclude(created__isnull=True)

    if querysets.exists():
        paginator = Paginator(querysets, 1000)
        total_page = paginator.num_pages

        for page_number in paginator.page_range:
            print(f'offices: processing page {page_number} of {total_page}')
            objs = paginator.page(page_number).object_list
            values = objs.values()
            batch_objects = []

            for row in values:
                row.pop('id')
                last_fetch_time = row['created']
                batch_objects.append(BackupOffices(**row))
            BackupOffices.objects.using('backup_source_db').bulk_create(batch_objects)

    print('backup office table complete')
    print()
    CURRENT_DATABASE_FETCH_TIME['offices'] = last_fetch_time


# Backup Users Table
def backup_users_table():
    last_fetched_date_object = TrackSourceDBLastFetchTime.objects.using('source_db').last()
    print('backup users table ...')

    last_fetch_time = None
    querysets = Users.objects.using('source_db').all()
    last_object = BackupUsers.objects.using('backup_source_db').last()

    # check users last fetch time from TrackSourceDBLastFetchTime Model
    # first time this will be absent.
    try:
        last_fetch_time = last_fetched_date_object.users
    except AttributeError:
        pass

    # if last fetch time absent again check from BackupOffices Model
    # first backup time this will be absent.
    # This check is done to avoid redundency
    if not last_fetch_time:
        try:
            last_fetch_time = last_object.created
        except AttributeError:
            pass

    if last_fetch_time:
        querysets = querysets.filter(created__gt=last_fetch_time)

    querysets = querysets.exclude(created__isnull=True)

    if querysets.exists():
        paginator = Paginator(querysets, 1000)
        total_page = paginator.num_pages

        for page_number in paginator.page_range:
            print(f'users: processing page {page_number} of {total_page}')
            objs = paginator.page(page_number).object_list
            values = objs.values()
            batch_objects = []

            for row in values:
                row.pop('id')
                last_fetch_time = row['created']
                batch_objects.append(BackupUsers(**row))
            BackupUsers.objects.using('backup_source_db').bulk_create(batch_objects)

    print('backup users table complete')
    print()

    CURRENT_DATABASE_FETCH_TIME['users'] = last_fetch_time


# Backup EmployeeRecords Table
def backup_employee_records_table():
    last_fetched_date_object = TrackSourceDBLastFetchTime.objects.using('source_db').last()
    print('backup employee_records table ...')

    last_fetch_time = None
    querysets = EmployeeRecords.objects.using('source_db').all()
    last_object = BackupEmployeeRecords.objects.using('backup_source_db').last()

    try:
        last_fetch_time = last_fetched_date_object.employee_records
    except AttributeError:
        pass

    # if last fetch time absent again check from BackupOffices Model
    # first backup time this will be absent.
    if not last_fetch_time:
        try:
            last_fetch_time = last_object.created
        except AttributeError:
            pass

    # first time backup this will be empty.
    # so we will backup whole table.
    if last_fetch_time:
        querysets = querysets.filter(created__gt=last_fetch_time)

    querysets = querysets.exclude(created__isnull=True)

    if querysets.exists():
        paginator = Paginator(querysets, 1000)
        total_page = paginator.num_pages

        for page_number in paginator.page_range:
            print(f'employee_records: processing page {page_number} of {total_page}')
            objs = paginator.page(page_number).object_list
            values = objs.values()
            batch_objects = []

            for row in values:
                row.pop('id')
                last_fetch_time = row['created']
                batch_objects.append(BackupEmployeeRecords(**row))
            BackupEmployeeRecords.objects.using('backup_source_db').bulk_create(batch_objects)

    print('backup employee_records table complete')
    print()
    CURRENT_DATABASE_FETCH_TIME['employee_records'] = last_fetch_time

# Backup NisponnoRecords Table
def backup_nisponno_records_table():
    last_fetched_date_object = TrackSourceDBLastFetchTime.objects.using('source_db').last()
    print('backup nisponno_records table ...')
    last_fetch_time = None
    querysets = NisponnoRecords.objects.using('source_db').all()
    backup_last_object = BackupNisponnoRecords.objects.using('backup_source_db').last()

    try:
        last_fetch_time = last_fetched_date_object.nisponno_records
    except AttributeError:
        pass

    if not last_fetch_time:
        try:
            last_fetch_time = backup_last_object.created
        except AttributeError:
            pass

    if not last_fetch_time:
        try:
            last_fetch_time = ReportNispottikrittoNothiModel.objects.last().report_day
            last_fetch_time = last_fetch_time + timedelta(days=1)
        except AttributeError:
            pass

    if last_fetch_time:
        querysets = querysets.filter(created__gt=last_fetch_time)

    querysets = querysets.exclude(created__isnull=True)

    if querysets.exists():
        paginator = Paginator(querysets, 1000)
        total_page = paginator.num_pages

        for page_number in paginator.page_range:
            print(f'nisponno_records: processing page {page_number} of {total_page}')
            objs = paginator.page(page_number).object_list
            values = objs.values()
            batch_objects = []

            for row in values:
                row.pop('id')
                last_fetch_time = row['created']
                batch_objects.append(BackupNisponnoRecords(**row))
            BackupNisponnoRecords.objects.using('backup_source_db').bulk_create(batch_objects)

    print('backup nisponno_records table complete')
    print()
    CURRENT_DATABASE_FETCH_TIME['nisponno_records'] = last_fetch_time


# Backup UserLoginHistory Table
def backup_user_login_history_table():
    last_fetched_date_object = TrackSourceDBLastFetchTime.objects.using('source_db').last()
    print('backup user_login_history table ...')
    last_fetch_time = None
    querysets = UserLoginHistory.objects.using('source_db').all()
    last_object = BackupUserLoginHistory.objects.using('backup_source_db').last()

    try:
        last_fetch_time = last_fetched_date_object.user_login_history
    except AttributeError:
        pass

    if not last_fetch_time:
        try:
            last_fetch_time = last_object.created
        except AttributeError:
            pass

    if not last_fetch_time:
        try:
            last_fetch_time = ReportLoginTotalUsers.objects.last().report_day
            last_fetch_time = last_fetch_time + timedelta(days=1)
        except AttributeError:
            pass

    if last_fetch_time:
        querysets = querysets.filter(created__gt=last_fetch_time)

    if querysets.exists():
        paginator = Paginator(querysets, 1000)
        total_page = paginator.num_pages

        for page_number in paginator.page_range:
            print(f'user_login_history: processing page {page_number} of {total_page}')
            objs = paginator.page(page_number).object_list
            values = objs.values()
            batch_objects = []

            for row in values:
                row.pop('id')
                last_fetch_time = row['created']
                batch_objects.append(BackupUserLoginHistory(**row))
            BackupUserLoginHistory.objects.using('backup_source_db').bulk_create(batch_objects)

    print('backup user_login_history table complete')
    print()
    CURRENT_DATABASE_FETCH_TIME['user_login_history'] = last_fetch_time


def update(request, *args, **kwargs):
    print()
    print('updating backup db ...')
    print()
    backup_office_table()
    backup_users_table()
    backup_employee_records_table()
    backup_nisponno_records_table()
    backup_user_login_history_table()
    TrackSourceDBLastFetchTime.objects.using('source_db').create(**CURRENT_DATABASE_FETCH_TIME)
    print()
    print('End backup db update')
    print()
