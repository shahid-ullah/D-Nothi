# automate_process/api.py
from datetime import datetime

from backup_source_db.models import BackupDBLog
from dashboard_generate.models import DashboardUpdateLog
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SourceDBLog, TrackSourceDBLastFetchTime
from .scripts import reports
from .serializers import (
    BackupDBLogSerializer,
    DatabaseBackupLogSerializer,
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

    def get(self, request, format=None, *args, **kwargs):
        """ """
        scripts_log = {}

        if settings.SYSTEM_UPDATE_RUNNING:
            print('system update running. please request later')
            return Response({'status': 'system update running. Please request later'})
        settings.SYSTEM_UPDATE_RUNNING = True

        try:
            reports.backup_source_database.update(request, *args, **kwargs)
            scripts_log['backup_db'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['backup_db'] = str(e)

        try:
            reports.total_offices.generate_report(request, *args, **kwargs)
            scripts_log['total_offices'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['total_offices'] = str(e)

        try:
            reports.nispottikritto_nothi.generate_report(request, *args, **kwargs)
            scripts_log['nispottikritto_nothi'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['nispottikritto_nothi'] = str(e)

        try:
            reports.upokarvogi.generate_report(request, *args, **kwargs)
            scripts_log['upokarvogi'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['upokarvogi'] = str(e)

        try:
            reports.potrojari.generate_report(request, *args, **kwargs)
            scripts_log['potrojari'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['potrojari'] = str(e)

        try:
            reports.note_nisponno.generate_report(request, *args, **kwargs)
            scripts_log['note_nisponno'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['note_nisponno'] = str(e)

        try:
            reports.total_nothi_users.generate_report(request, *args, **kwargs)
            scripts_log['total_nothi_users'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['total_nothi_users'] = str(e)

        try:
            reports.male_female_nothi_users.generate_report(request, *args, **kwargs)
            scripts_log['male_female_nothi_users'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['male_female_nothi_users'] = str(e)

        try:
            reports.mobile_app_users.generate_report(request, *args, **kwargs)
            scripts_log['mobile_app_users'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['mobile_app_users'] = str(e)

        try:
            reports.android_ios_users.generate_report(request, *args, **kwargs)
            scripts_log['android_ios_users'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['android_ios_users'] = str(e)

        try:
            reports.login_total_users.generate_report(request, *args, **kwargs)
            scripts_log['login_total_users'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['login_total_users'] = str(e)

        try:
            reports.login_total_users_not_distinct.generate_report(request, *args, **kwargs)
            scripts_log['login_total_users_not_distinct'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['login_total_users_not_distinct'] = str(e)

        try:
            reports.login_male_female_users.generate_report(request, *args, **kwargs)
            scripts_log['login_male_female_users'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['login_male_female_users'] = str(e)

        try:
            DashboardUpdateLog.objects.create(
                completion_log='empty,',
                user=self.request.user,
                status=scripts_log,
                update_start_time=datetime.now(),
                update_completion_time=datetime.now(),
            )
            scripts_log['dashboard_update_log'] = 'success'
        except Exception as e:
            scripts_log['dashboard_update_log'] = str(e)
            print(e)

        try:
            reports.utils.update_backup_db_log(request, *args, **kwargs)
            scripts_log['backup_db_log'] = 'success'
        except Exception as e:
            print(e)
            scripts_log['backup_db_log'] = str(e)

        settings.SYSTEM_UPDATE_RUNNING = False

        return Response(scripts_log)


class DatabaseBackupLog(mixins.ListModelMixin, generics.GenericAPIView):
    # queryset = TrackSourceDBLastFetchTime.objects.using('source_db').all()
    queryset = SourceDBLog.objects.using('source_db').all().order_by('-id')
    serializer_class = DatabaseBackupLogSerializer
    authentication_classes = [authentication.SessionAuthentication]

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SourceDBLogAPI(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = SourceDBLog.objects.using('source_db').all().order_by('-id')
    serializer_class = SourceDBLogSerializer
    authentication_classes = [authentication.SessionAuthentication]

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BackupDBLogAPI(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = BackupDBLog.objects.using('backup_source_db').all().order_by('-id')
    serializer_class = BackupDBLogSerializer
    authentication_classes = [authentication.SessionAuthentication]

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
