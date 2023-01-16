# automate_process/api.py

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from automate_process.models import EmployeeRecords, NisponnoRecords, Offices, UserLoginHistory, Users
from backup_source_db.models import BackupDBLog
from dashboard_generate.models import (
    ReportGenerationLog,
    ReportLoginFemalelUsersModel,
    ReportLoginMalelUsersModel,
    ReportLoginTotalUsers,
    ReportLoginTotalUsersNotDistinct,
)

from .models import SourceDBLog
from .scripts import reports
from .serializers import (
    BackupDBLogSerializer,
    DatabaseBackupLogSerializer,
    ReportGenerationLogSerializer,
    SourceDBLogSerializer,
)

User = get_user_model()


class updateDashboard(APIView):
    """
    update dashboard data.
    process source db data and dump to dashboard db.
    Table: OFFICES
        1. total_offices
    Table: NISPONNORECORDS
        1. nispottikritto_nothi
        2. upokarvogi
        3. potrojari
        4. note_nisponno
    Table: USERS
        1. total_nothi_users
    Table: USERS_EMPLOYEE_RECORDS
        1. male nothi users
        2. female nothi users
    Table: USER_LOGIN_HISTORY
        1. mobile_app_users
        2. android_ios_users
        3. login_total_users
    Table: USER_LOGIN_HISTORY_EMPLOYEE_RECORDS
        1. login_male_users
        2. login_female_users
    """

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def get(self, request, format=None, *args, **kwargs):

        if settings.SYSTEM_UPDATE_RUNNING:
            print('system update running. please request later')
            return Response({'status': 'system update running. Please request later'})
        settings.SYSTEM_UPDATE_RUNNING = True

        self.generate_report(request, *args, **kwargs)
        self._backup_source_db(request, *args, **kwargs)
        print(self.scripts_log)

        settings.SYSTEM_UPDATE_RUNNING = False

        return Response(self.scripts_log)

    def _backup_source_db(self, request, *args, **kwargs):
        try:
            reports.backup_source_database.update(request, *args, **kwargs)
            self.scripts_log['backup_db'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['backup_db'] = str(e)

        try:
            reports.utils.update_backup_db_log(request, *args, **kwargs)
            self.scripts_log['backup_db_log'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['backup_db_log'] = str(e)

    def cache_currrent_report_generation_log(self, request, *args, **kwargs):
        self.queryset_user_login_history = UserLoginHistory.objects.using('source_db').filter(created__isnull=False)
        self.queryset_users = Users.objects.using('source_db').filter(created__isnull=False)
        self.queryset_employee_records = EmployeeRecords.objects.using('source_db').filter(created__isnull=False)
        self.queryset_offices = Offices.objects.using('source_db').filter(created__isnull=False)
        self.queryset_nisponno_records = NisponnoRecords.objects.using('source_db').filter(created__isnull=False)

        self.currrent_report_generation_log['last_user_id'] = self.queryset_users.last().id
        self.currrent_report_generation_log['last_office_id'] = self.queryset_offices.last().id
        self.currrent_report_generation_log['last_employee_id'] = self.queryset_employee_records.last().id
        self.currrent_report_generation_log['last_login_history_time'] = self.queryset_user_login_history.last().created
        self.currrent_report_generation_log[
            'last_nisponno_records_time'
        ] = self.queryset_nisponno_records.last().created

        self.scripts_log['table_last_entry'] = self.currrent_report_generation_log

    def update_report_generation_log(self, request, *args, **kwargs):
        object_dict = {}
        object_dict['last_office_id'] = self.currrent_report_generation_log['last_office_id']
        object_dict['last_user_id'] = self.currrent_report_generation_log['last_user_id']
        object_dict['last_employee_id'] = self.currrent_report_generation_log['last_employee_id']
        object_dict['last_login_history_time'] = self.currrent_report_generation_log['last_login_history_time']
        object_dict['last_nisponno_records_time'] = self.currrent_report_generation_log['last_nisponno_records_time']
        object_dict['status'] = str(self.scripts_log)
        ReportGenerationLog.objects.create(**object_dict)

    def initialize_variables(self, request, *args, **kwargs):
        self.currrent_report_generation_log = {}
        self.scripts_log = {}

    def set_users_querysets(self, request, *args, **kwargs):
        # At first creation last log will be None
        last_log = ReportGenerationLog.objects.last()
        querysets = self.queryset_users

        try:
            last_user_id = int(last_log.last_user_id)
            querysets = querysets.filter(id__gt=last_user_id)
        except Exception as e:
            querysets = None

        self.users_querysets = querysets

    def set_offices_querysets(self, request, *args, **kwargs):
        # At first creation last log will be None
        last_log = ReportGenerationLog.objects.last()
        querysets = self.queryset_offices

        try:
            last_office_id = int(last_log.last_office_id)
            querysets = querysets.filter(id__gt=last_office_id)
        except Exception as e:
            querysets = None

        self.offices_querysets = querysets

    def set_user_login_history_querysets(self, request, *args, **kwargs):
        # At first creation last log will be None
        last_log = ReportGenerationLog.objects.last()
        querysets = self.queryset_user_login_history

        try:
            last_login_history_time = last_log.last_login_history_time
            if last_login_history_time:
                querysets = querysets.filter(created__gt=last_login_history_time)
            else:
                querysets = None
        except Exception as e:
            querysets = None

        self.user_login_history_querysets = querysets

    def set_nisponno_records_querysets(self, request, *args, **kwargs):
        # At first creation last log will be None
        last_log = ReportGenerationLog.objects.last()
        querysets = self.queryset_nisponno_records

        try:
            last_nisponno_records_time = last_log.last_nisponno_records_time
            if last_nisponno_records_time:
                querysets = querysets.filter(created__gt=last_nisponno_records_time)
            else:
                querysets = None
        except Exception as e:
            querysets = None

        self.nisponno_records_querysets = querysets

    def setup_base_querysets(self, request, *args, **kwargs):
        self.set_users_querysets(request, *args, **kwargs)
        self.set_offices_querysets(request, *args, **kwargs)
        self.set_user_login_history_querysets(request, *args, **kwargs)
        self.set_nisponno_records_querysets(request, *args, **kwargs)

    def generate_report(self, request, *args, **kwargs):
        # self.clear_report_tables(request, *args, **kwargs)
        self.initialize_variables(request, *args, **kwargs)
        self.cache_currrent_report_generation_log(request, *args, **kwargs)
        self.setup_base_querysets(request, *args, **kwargs)

        self.generate_total_offices_report(request, *args, **kwargs)
        self.generate_nispottikritto_nothi_report(request, *args, **kwargs)
        self.generate_upokarvogi_report(request, *args, **kwargs)
        self.generate_potrojari_report(request, *args, **kwargs)
        self.generate_note_nisponno_report(request, *args, **kwargs)
        self.generate_total_nothi_users_report(request, *args, **kwargs)
        self.generate_male_female_users_report(request, *args, **kwargs)
        self.generate_mobile_app_users_report(request, *args, **kwargs)
        self.generate_android_ios_users_report(request, *args, **kwargs)
        self.generate_login_total_users_report(request, *args, **kwargs)
        self.generate_login_total_users_not_distinct_report(request, *args, **kwargs)
        self.generate_login_male_female_users_report(request, *args, **kwargs)

        self.update_report_generation_log(request, *args, **kwargs)

    def generate_total_offices_report(self, request, *args, **kwargs):
        try:
            kwargs['querysets'] = self.offices_querysets
            reports.total_offices.generate_report(request, *args, **kwargs)
            self.scripts_log['total_offices'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['total_offices'] = str(e)

    def generate_nispottikritto_nothi_report(self, request, *args, **kwargs):
        kwargs['querysets'] = self.nisponno_records_querysets
        try:
            reports.nispottikritto_nothi.generate_report(request, *args, **kwargs)
            self.scripts_log['nispottikritto_nothi'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['nispottikritto_nothi'] = str(e)

    def generate_upokarvogi_report(self, request, *args, **kwargs):
        try:
            kwargs['querysets'] = self.nisponno_records_querysets
            reports.upokarvogi.generate_report(request, *args, **kwargs)
            self.scripts_log['upokarvogi'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['upokarvogi'] = str(e)

    def generate_potrojari_report(self, request, *args, **kwargs):
        try:
            kwargs['querysets'] = self.nisponno_records_querysets
            reports.potrojari.generate_report(request, *args, **kwargs)
            self.scripts_log['potrojari'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['potrojari'] = str(e)

    def generate_note_nisponno_report(self, request, *args, **kwargs):
        try:
            kwargs['querysets'] = self.nisponno_records_querysets
            reports.note_nisponno.generate_report(request, *args, **kwargs)
            self.scripts_log['note_nisponno'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['note_nisponno'] = str(e)

    def generate_total_nothi_users_report(self, request, *args, **kwargs):
        try:
            kwargs['querysets'] = self.users_querysets
            reports.total_nothi_users.generate_report(request, *args, **kwargs)
            self.scripts_log['total_nothi_users'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['total_nothi_users'] = str(e)

    def generate_male_female_users_report(self, request, *args, **kwargs):
        try:
            kwargs['querysets'] = self.users_querysets
            reports.male_female_nothi_users.generate_report(request, *args, **kwargs)
            self.scripts_log['male_female_nothi_users'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['male_female_nothi_users'] = str(e)

    def generate_mobile_app_users_report(self, request, *args, **kwargs):
        try:
            kwargs['querysets'] = self.user_login_history_querysets
            reports.mobile_app_users.generate_report(request, *args, **kwargs)
            self.scripts_log['mobile_app_users'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['mobile_app_users'] = str(e)

    def generate_android_ios_users_report(self, request, *args, **kwargs):
        try:
            kwargs['querysets'] = self.user_login_history_querysets
            reports.android_ios_users.generate_report(request, *args, **kwargs)
            self.scripts_log['android_ios_users'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['android_ios_users'] = str(e)

    def generate_login_total_users_report(self, request, *args, **kwargs):
        try:
            kwargs['querysets'] = self.user_login_history_querysets
            reports.login_total_users.generate_report(request, *args, **kwargs)
            self.scripts_log['login_total_users'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['login_total_users'] = str(e)

    def generate_login_total_users_not_distinct_report(self, request, *args, **kwargs):
        try:
            kwargs['querysets'] = self.user_login_history_querysets
            reports.login_total_users_not_distinct.generate_report(request, *args, **kwargs)
            self.scripts_log['login_total_users_not_distinct'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['login_total_users_not_distinct'] = str(e)

    def generate_login_male_female_users_report(self, request, *args, **kwargs):
        try:
            kwargs['querysets'] = self.user_login_history_querysets
            reports.login_male_female_users.generate_report(request, *args, **kwargs)
            self.scripts_log['login_male_female_users'] = 'success'
        except Exception as e:
            print(e)
            self.scripts_log['login_male_female_users'] = str(e)

    def clear_report_tables(self, request, *args, **kwargs):
        if settings.DEBUG:
            ReportGenerationLog.objects.all().delete()
            ReportLoginMalelUsersModel.objects.all().delete()
            ReportLoginFemalelUsersModel.objects.all().delete()
            ReportLoginTotalUsers.objects.all().delete()
            ReportLoginTotalUsersNotDistinct.objects.all().delete()


class ReportGenerationLogAPI(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = ReportGenerationLog.objects.all().order_by('-id')
    serializer_class = ReportGenerationLogSerializer
    authentication_classes = [authentication.SessionAuthentication]

    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DatabaseBackupLog(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = SourceDBLog.objects.using('source_db').all().order_by('-id')
    serializer_class = DatabaseBackupLogSerializer
    authentication_classes = [authentication.SessionAuthentication]

    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SourceDBLogAPI(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = SourceDBLog.objects.using('source_db').all().order_by('-id')
    serializer_class = SourceDBLogSerializer
    authentication_classes = [authentication.SessionAuthentication]

    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BackupDBLogAPI(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = BackupDBLog.objects.using('backup_source_db').all().order_by('-id')
    serializer_class = BackupDBLogSerializer
    authentication_classes = [authentication.SessionAuthentication]

    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
