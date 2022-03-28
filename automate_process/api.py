# automate_process/api.py
import time
from datetime import datetime

import pandas as pd
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
        offices_objects = Offices.objects.using('source_db').all()
        offices_values = offices_objects.values('id', 'active_status',
                                                'created')
        offices_dataframe = pd.DataFrame(offices_values)
        total_offices_status = reports.total_offices.update(
            offices_dataframe, request)
        status['offices']['total_offices'] = total_offices_status
        offices_objects = None
        offices_values = None
        offices_dataframe = None

        # Table 2: nisponno_records
        status['nisponno_records'] = {}
        nisponno_records_objects = NisponnoRecords.objects.using(
            'source_db').all()
        nisponno_records_values = nisponno_records_objects.values(
            'id', 'type', 'upokarvogi', 'operation_date')
        nisponno_records_dataframe = pd.DataFrame(nisponno_records_values)
        # nispottikritto_nothi
        status_ = reports.nispottikritto_nothi.update(
            nisponno_records_dataframe, request)
        status['nisponno_records']['nispottikritto_nothi'] = status_
        # upokarvogi
        status_ = reports.upokarvogi.update(nisponno_records_dataframe,
                                            request)
        status['nisponno_records']['upokarvogi'] = status_
        # potrojari
        status_ = reports.potrojari.update(nisponno_records_dataframe, request)
        status['nisponno_records']['potrojari'] = status_
        # note nisponno
        status_ = reports.note_nisponno.update(nisponno_records_dataframe,
                                               request)
        status['nisponno_records']['note_nisponno'] = status_
        nisponno_records_objects = None
        nisponno_records_values = None
        nisponno_records_dataframe = None

        # Table 3: users
        status['users'] = {}
        users_objects = Users.objects.using('source_db').all()
        users_values = users_objects.values(
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
        users_dataframe = pd.DataFrame(users_values)
        status_ = reports.total_nothi_users.update(users_dataframe, request)
        status['users']['total_nothi_users'] = status_

        # Table 4: users_employee_records
        status['users_employee_records'] = {}
        employee_records_objects = EmployeeRecords.objects.using(
            'source_db').all()
        employee_records_values = employee_records_objects.values(
            'id', 'name_eng', 'gender', 'created', 'modified')
        employee_records_dataframe = pd.DataFrame(employee_records_values)
        # male_female_users
        status_ = reports.male_female_nothi_users.update(
            request, users_dataframe, employee_records_dataframe)
        status['users_employee_records'] = status_

        users_objects = None
        users_values = None
        users_dataframe = None
        employee_records_objects = None
        employee_records_values = None
        # employee_records_dataframe = None

        # Table 5: user_login_history

        status['user_login_history'] = {}
        login_history_objects = UserLoginHistory.objects.using(
            'source_db').all()
        login_history_values = login_history_objects.values(
            'id', 'is_mobile', 'created', 'employee_record_id', 'device_type')
        login_history_dataframe = pd.DataFrame(login_history_values)
        # mobile_app_users
        status_ = reports.mobile_app_users.update(login_history_dataframe,
                                                  request)
        status['user_login_history']['mobile_app_users'] = status_
        # Android-IOS users
        status_ = reports.android_ios_users.update(login_history_dataframe,
                                                   request)
        status['user_login_history']['android_ios_users'] = status_
        # Login Total users
        st = reports.login_total_users.update(login_history_dataframe, request)
        status['user_login_history']['login_total_users'] = st

        # Table 6: user_login_history_employee_records
        # login_male_female_nothi_users
        status['user_login_history_employee_records'] = {}
        male_status, female_status = reports.login_male_female_users.update(
            request, login_history_dataframe, employee_records_dataframe)
        status['user_login_history_employee_records'][
            'login_male_users'] = male_status
        status['user_login_history_employee_records'][
            'login_female_users'] = female_status
        employee_records_objects = None
        employee_records_values = None
        employee_records_dataframe = None
        login_history_objects = None
        login_history_values = None
        login_history_dataframe = None

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
