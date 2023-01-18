from datetime import timedelta

from django.core.paginator import Paginator

from automate_process.models import EmployeeRecords, NisponnoRecords, Offices, SourceDBLog, UserLoginHistory, Users
from backup_source_db.models import (
    BackupDBLog,
    BackupEmployeeRecords,
    BackupNisponnoRecords,
    BackupOffices,
    BackupUserLoginHistory,
    BackupUsers,
)
from dashboard_generate.models import ReportLoginTotalUsers, ReportNispottikrittoNothiModel

print('Loading backup_source_db scripts')


class BackupSourceDB:
    # Backup Offices Table
    def __init__(self):
        self.BACKUP_LOG = {}
        self.initialize_source_db_object()

    def initialize_source_db_object(self):
        self.source_db_object = SourceDBLog.objects.create()

    def update_source_db_object(self):
        try:
            for key, value in self.BACKUP_LOG.items():
                setattr(self.source_db_object, key, value)
            self.source_db_object.save()
        except Exception as e:
            print(e)

    def update_backup_db_log(self):
        try:
            BackupDBLog.objects.using('backup_source_db').create(**self.BACKUP_LOG)
        except Exception as e:
            print(e)

    def backup_office_table(self, *args, **kwargs):
        print('backup offices table ...')
        querysets = Offices.objects.using('source_db').all()
        latest_office_id = querysets.last().id
        last_office = BackupOffices.objects.using('backup_source_db').last()

        # get new registered offices if any
        # get last registered office id from backup database
        try:
            last_office_id = last_office.source_id
            querysets = querysets.filter(id__gt=last_office_id)
        except:
            pass

        if querysets.exists():
            paginator = Paginator(querysets, 1000)
            total_page = paginator.num_pages

            for page_number in paginator.page_range:
                print(f'offices: processing page {page_number} of {total_page}')
                objs = paginator.page(page_number).object_list
                values = objs.values()
                batch_objects = []

                for row in values:
                    source_id = row.pop('id')
                    row['source_id'] = source_id
                    batch_objects.append(BackupOffices(**row))
                BackupOffices.objects.using('backup_source_db').bulk_create(batch_objects)

        print('backup office table complete')
        print()
        self.BACKUP_LOG['last_office_id'] = latest_office_id

    # Backup Users Table
    def backup_users_table(self, *args, **kwargs):
        print('backup users table ...')
        querysets = Users.objects.using('source_db').all()
        latest_user_id = querysets.last().id
        last_user = BackupUsers.objects.using('backup_source_db').last()

        try:
            last_user_id = last_user.source_id
            querysets = querysets.filter(id__gt=last_user_id)
        except:
            pass

        if querysets.exists():
            paginator = Paginator(querysets, 1000)
            total_page = paginator.num_pages

            for page_number in paginator.page_range:
                print(f'users: processing page {page_number} of {total_page}')
                objs = paginator.page(page_number).object_list
                values = objs.values()
                batch_objects = []

                for row in values:
                    source_id = row.pop('id')
                    row['source_id'] = source_id
                    batch_objects.append(BackupUsers(**row))
                BackupUsers.objects.using('backup_source_db').bulk_create(batch_objects)

        print('backup users table complete')
        print()
        self.BACKUP_LOG['last_user_id'] = latest_user_id

    def backup_employee_records_table(self, *args, **kwargs):
        print('backup employee_records table ...')
        querysets = EmployeeRecords.objects.using('source_db').all()
        latest_employee_id = querysets.last().id
        last_employee = BackupEmployeeRecords.objects.using('backup_source_db').last()

        try:
            last_employee_id = last_employee.source_id
            querysets = querysets.filter(id__gt=last_employee_id)
        except:
            pass

        if querysets.exists():
            paginator = Paginator(querysets, 1000)
            total_page = paginator.num_pages

            for page_number in paginator.page_range:
                print(f'employee_records: processing page {page_number} of {total_page}')
                objs = paginator.page(page_number).object_list
                values = objs.values()
                batch_objects = []

                for row in values:
                    source_id = row.pop('id')
                    row['source_id'] = source_id
                    batch_objects.append(BackupEmployeeRecords(**row))
                BackupEmployeeRecords.objects.using('backup_source_db').bulk_create(batch_objects)

        print('backup employee_records table complete')
        print()
        self.BACKUP_LOG['last_employee_id'] = latest_employee_id

    def backup_nisponno_records_table(self, *args, **kwargs):
        last_fetched_date_object = BackupDBLog.objects.using('backup_source_db').last()
        print('backup nisponno_records table ...')
        last_fetch_time = None
        querysets = NisponnoRecords.objects.using('source_db').all()
        backup_last_object = BackupNisponnoRecords.objects.using('backup_source_db').last()

        try:
            last_fetch_time = last_fetched_date_object.last_nisponno_records_time
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
                    source_id = row.pop('id')
                    row['source_id'] = source_id
                    last_fetch_time = row['created']
                    batch_objects.append(BackupNisponnoRecords(**row))
                BackupNisponnoRecords.objects.using('backup_source_db').bulk_create(batch_objects)

        print('backup nisponno_records table complete')
        print()
        self.BACKUP_LOG['last_nisponno_records_time'] = last_fetch_time

    # Backup UserLoginHistory Table
    def backup_user_login_history_table(self, *args, **kwargs):
        last_fetched_date_object = BackupDBLog.objects.using('backup_source_db').last()
        print('backup user_login_history table ...')
        last_fetch_time = None
        querysets = UserLoginHistory.objects.using('source_db').all()
        last_object = BackupUserLoginHistory.objects.using('backup_source_db').last()

        try:
            last_fetch_time = last_fetched_date_object.last_login_history_time
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
                    source_id = row.pop('id')
                    row['source_id'] = source_id
                    last_fetch_time = row['created']
                    batch_objects.append(BackupUserLoginHistory(**row))
                BackupUserLoginHistory.objects.using('backup_source_db').bulk_create(batch_objects)

        print('backup user_login_history table complete')
        print()
        self.BACKUP_LOG['last_login_history_time'] = last_fetch_time


def update(request, *args, **kwargs):
    backupdb_object = BackupSourceDB()

    print()
    print('updating backup db ...')
    print()
    try:
        backupdb_object.backup_office_table()
    except Exception as e:
        print('backup_office_table failed: ', str(e))

    try:
        backupdb_object.backup_users_table()
    except Exception as e:
        print('backup_users_table failed: ', str(e))

    try:
        backupdb_object.backup_employee_records_table()
    except Exception as e:
        print('backup_employee_records_table failed: ', str(e))

    try:
        backupdb_object.backup_nisponno_records_table()
    except Exception as e:
        print('backup_nisponno_records_table failed: ', str(e))

    try:
        backupdb_object.backup_user_login_history_table()
    except Exception as e:
        print('backup_user_login_historty failed: ', str(e))

    # SourceDBLog.objects.create(**backupdb_object.BACKUP_LOG)
    backupdb_object.update_source_db_object()
    backupdb_object.update_backup_db_log()

    print()
    print('End backup db update')
    print()
