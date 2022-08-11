from datetime import timedelta

from django.core.paginator import Paginator

from automate_process.models import (EmployeeRecords, NisponnoRecords, Offices,
                                     TrackSourceDBLastFetchTime,
                                     UserLoginHistory, Users)
from backup_source_db.models import (BackupEmployeeRecords,
                                     BackupNisponnoRecords, BackupOffices,
                                     BackupUserLoginHistory, BackupUsers)

last_fetched_date_object = TrackSourceDBLastFetchTime.objects.using('source_db').last()

print('Loading backup_source_db scripts')

CURRENT_DATABASE_FETCH_TIME = {}

# Backup Offices Table
def backup_office_table():
    print('backup offices table ...')
    queryset = None
    last_fetch_time = None

    try:
        last_fetch_time = last_fetched_date_object.offices
    except AttributeError:
        last_fetch_time = None

    if last_fetch_time:
        queryset = Offices.objects.using('source_db').filter(created__gt=last_fetch_time)
        queryset = queryset.exclude(created__isnull=True)
    else:
        queryset = Offices.objects.using('source_db').exclude(created__isnull=True)

    if queryset.exists():
        paginator = Paginator(queryset, 1000)
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
    CURRENT_DATABASE_FETCH_TIME['offices'] = last_fetch_time


# Backup Users Table
def backup_users_table():
    print('backup users table ...')
    queryset = None
    last_fetch_time = None

    try:
        last_fetch_time = last_fetched_date_object.users
    except AttributeError:
        last_fetch_time = None

    if last_fetch_time:
        queryset = Users.objects.using('source_db').filter(created__gt=last_fetch_time)
        queryset = queryset.exclude(created__isnull=True)
    else:
        queryset = Users.objects.using('source_db').exclude(created__isnull=True)

    if queryset.exists():
        paginator = Paginator(queryset, 1000)
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
    CURRENT_DATABASE_FETCH_TIME['users'] = last_fetch_time


# Backup EmployeeRecords Table
def backup_employee_records_table():
    print('backup employee_records table ...')
    queryset = None
    last_fetch_time = None

    try:
        last_fetch_time = last_fetched_date_object.employee_records
    except AttributeError:
        last_fetch_time = None

    if last_fetch_time:
        queryset = EmployeeRecords.objects.using('source_db').filter(created__gt=last_fetch_time)
        queryset = queryset.exclude(created__isnull=True)
    else:
        queryset = EmployeeRecords.objects.using('source_db').exclude(created__isnull=True)

    if queryset.exists():
        paginator = Paginator(queryset, 1000)
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
    CURRENT_DATABASE_FETCH_TIME['employee_records'] = last_fetch_time

# Backup NisponnoRecords Table
def backup_nisponno_records_table():
    print('backup nisponno_records table ...')
    last_fetch_time = None
    queryset = None

    try:
        last_fetch_time = last_fetched_date_object.nisponno_records
        queryset = NisponnoRecords.objects.using('source_db').all()
        queryset = queryset.filter(created__gt=last_fetch_time)
        queryset = queryset.exclude(created__isnull=True)
    except AttributeError:
        queryset = NisponnoRecords.objects.using('source_db').all()
        queryset = queryset.exclude(created__isnull=True)
        if queryset.exists():
            last_fetch_time = queryset.last().created - timedelta(days=7)
            queryset = queryset.filter(created__gt=last_fetch_time)

    if queryset.exists():
        paginator = Paginator(queryset, 1000)
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
    CURRENT_DATABASE_FETCH_TIME['nisponno_records'] = last_fetch_time


# Backup UserLoginHistory Table
def backup_user_login_history_table():
    print('backup user_login_history table ...')
    last_fetch_time = None
    queryset = None

    try:
        last_fetch_time = last_fetched_date_object.user_login_history
        queryset = UserLoginHistory.objects.using('source_db').all()
        queryset = queryset.filter(created__gt=last_fetch_time)
        queryset = queryset.exclude(created__isnull=True)
    except AttributeError:
        queryset = UserLoginHistory.objects.using('source_db').all()
        queryset = queryset.exclude(created__isnull=True)
        if queryset.exists():
            last_fetch_time = queryset.last().created - timedelta(days=7)
            queryset = queryset.filter(created__gt=last_fetch_time)

    if queryset.exists():
        paginator = Paginator(queryset, 1000)
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
    CURRENT_DATABASE_FETCH_TIME['user_login_history'] = last_fetch_time

def backup_source_tables():
    backup_office_table()
    backup_users_table()
    backup_employee_records_table()
    backup_nisponno_records_table()
    backup_user_login_history_table()
    TrackSourceDBLastFetchTime.objects.using('source_db').create(**CURRENT_DATABASE_FETCH_TIME)

    return None

try:
    backup_source_tables()
except Exception as e:
    print('Error occured while backup source tables')



# CURRENT_DATABASE_FETCH_TIME['offices'] = CURRENT_DATABASE_FETCH_TIME['offices']
# CURRENT_DATABASE_FETCH_TIME['users'] = CURRENT_DATABASE_FETCH_TIME['offices']
# CURRENT_DATABASE_FETCH_TIME['employee_records'] = CURRENT_DATABASE_FETCH_TIME['offices']
# CURRENT_DATABASE_FETCH_TIME['nisponno_records'] = CURRENT_DATABASE_FETCH_TIME['offices']
# CURRENT_DATABASE_FETCH_TIME['user_login_history'] = CURRENT_DATABASE_FETCH_TIME['offices']

