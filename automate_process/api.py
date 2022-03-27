# automate_process/api.py
import time
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard_generate.models import DashboardUpdateLog

from .models import (EmployeeRecords, NisponnoRecords, Offices,
                     UserLoginHistory, Users)
from .scripts import reports

User = get_user_model()


class updateDashboard(APIView):
    """
    update dashboard data.
    process source db data and dump to dashboard db.
    """

    # authentication_classes = [authentication.SessionAuthentication]

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """ """

        status = {}
        if settings.SYSTEM_UPDATE_RUNNING:
            print('system update running. please request later')
            return Response(
                {'status': 'system update running. Please request later'})

        start_processing_time = time.perf_counter()
        update_start_time = datetime.now(),
        settings.SYSTEM_UPDATE_RUNNING = True
        try:
            update_log_object = DashboardUpdateLog.objects.create(
                user=self.request.user,
                status=status,
                update_start_time=datetime.now(),
            )
        except Exception as e:
            print(e)

        # Table 1: offices

        status['offices'] = {}
        o_objs = Offices.objects.using('source_db').all()[:100]
        o_values = o_objs.values('id', 'active_status', 'created')
        total_offices_status = reports.total_offices.update(o_values, request)
        status['offices']['total_offices'] = total_offices_status
        o_values = None

        # Table 2: nisponno_records
        status['nisponno_records'] = {}
        nr_objs = NisponnoRecords.objects.using('source_db').all()[:100]
        nr_values = nr_objs.values('id', 'type', 'upokarvogi',
                                   'operation_date')
        # nispottikritto_nothi
        ni_status = reports.nispottikritto_nothi.update(nr_values, request)
        status['nisponno_records']['nispottikritto_nothi'] = ni_status
        # upokarvogi
        st = reports.upokarvogi.update(nr_values, request)
        status['nisponno_records']['upokarvogi'] = st
        # potrojari
        st = reports.potrojari.update(nr_values, request)
        status['nisponno_records']['potrojari'] = st
        # note nisponno
        st = reports.note_nisponno.update(nr_values, request)
        status['nisponno_records']['note_nisponno'] = st
        nr_values = None

        # Table 3: users
        status['users'] = {}
        u_objs = Users.objects.using('source_db').all()[:100]
        u_values = u_objs.values(
            'id',
            'username',
            'user_role_id',
            'is_admin',
            'active',
            'user_status',
            'created',
            'modified',
            'employee_record_id',
        )
        st = reports.total_nothi_users.update(u_values, request)
        status['users']['total_nothi_users'] = st
        # u_values = None

        # Table 4: users_employee_records
        status['users_employee_records'] = {}
        er_objs = EmployeeRecords.objects.using('source_db').all()[:100]
        er_values = er_objs.values('id', 'name_eng', 'gender', 'created',
                                   'modified')
        # male_female_users
        st = reports.male_female_nothi_users.update(request, u_values,
                                                    er_values)
        status['users_employee_records'] = st

        # Table 5: user_login_history

        status['user_login_history'] = {}
        lh_objs = UserLoginHistory.objects.using('source_db').all()[:100]
        lh_values = lh_objs.values('id', 'is_mobile', 'created',
                                   'employee_record_id')
        # mobile_app_users
        st = reports.mobile_app_users.update(lh_values, request)
        status['user_login_history']['mobile_app_users'] = st
        # Android-IOS users
        st = reports.android_ios_users.update(lh_values, request)
        status['user_login_history']['android_ios_users'] = st
        # Login Total users
        st = reports.login_total_users.update(lh_values, request)
        status['user_login_history']['login_total_users'] = st

        # Table 6: user_login_history_employee_records

        # login_male_female_nothi_users
        status['user_login_history_employee_records'] = {}
        st1, st2 = reports.login_male_female_users.update(
            request, lh_values, er_values)
        status['user_login_history_employee_records']['login_male_users'] = st1
        status['user_login_history_employee_records'][
            'login_female_users'] = st2

        settings.SYSTEM_UPDATE_RUNNING = False
        end_processing_time = time.perf_counter()
        status[
            'computation_time'] = end_processing_time - start_processing_time

        try:
            update_log_object.status = status
            update_log_object.update_completion_time = datetime.now()
            update_log_object.save()
        except Exception as e:
            print(e)

        return Response(status)
