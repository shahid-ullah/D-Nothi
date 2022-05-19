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
    Table: Offices
        1. total_offices
    Table: NisponnoRecords
        1. nispottikritto_nothi
        2. upokarvogi
        3. potrojari
        4. note_nisponno
    Table: Users
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

    def update_log(self, request, object, process_running, total_process, status={}):
        if process_running:
            completion_log = f"process running {process_running} of {total_process}"
            print(completion_log)
        else:
            completion_log = f"process completed {total_process} of {total_process}"
            print(completion_log)
        try:
            if not object:
                object = DashboardUpdateLog.objects.create(
                    user=self.request.user,
                    completion_log=completion_log,
                    status=status,
                    update_start_time=datetime.now(),
                )
            else:
                object.completion_log = completion_log,
                object.status = status
                object.update_completion_time = datetime.now()
                object.save()

            return object
        except Exception as e:
            print(e)

    def get(self, request, format=None):
        """ """

        status = {}
        total_process = 13
        if settings.SYSTEM_UPDATE_RUNNING:
            print('system update running. please request later')
            return Response({'status': 'system update running. Please request later'})

        start_processing_time = time.perf_counter()
        settings.SYSTEM_UPDATE_RUNNING = True

        object = self.update_log(request, object=None, process_running=1, total_process=total_process)

        # Table 1: offices

        status['offices'] = {}
        offices_objects = Offices.objects.using('source_db').all()
        offices_values = offices_objects.values('id', 'active_status', 'created')
        offices_dataframe = pd.DataFrame(offices_values)
        total_offices_status = reports.total_offices.update(offices_dataframe, request)
        status['offices']['total_offices'] = total_offices_status
        offices_objects = None
        offices_values = None
        offices_dataframe = None
        object = self.update_log(request, object=object, process_running=2, total_process=total_process)

        # Table 2: nisponno_records
        status['nisponno_records'] = {}
        nisponno_records_objects = NisponnoRecords.objects.using('source_db').all()
        nisponno_records_values = nisponno_records_objects.values(
            'id', 'type', 'upokarvogi', 'operation_date'
        )
        nisponno_records_dataframe = pd.DataFrame(nisponno_records_values)
        # nispottikritto_nothi
        status_ = reports.nispottikritto_nothi.update(
            nisponno_records_dataframe, request
        )
        status['nisponno_records']['nispottikritto_nothi'] = status_
        object = self.update_log(request, object=object, process_running=3, total_process=total_process)

        # upokarvogi
        status_ = reports.upokarvogi.update(nisponno_records_dataframe, request)
        status['nisponno_records']['upokarvogi'] = status_
        object = self.update_log(request, object=object, process_running=4, total_process=total_process)
        # potrojari
        status_ = reports.potrojari.update(nisponno_records_dataframe, request)
        status['nisponno_records']['potrojari'] = status_
        object = self.update_log(request, object=object, process_running=5, total_process=total_process)
        # note nisponno
        status_ = reports.note_nisponno.update(nisponno_records_dataframe, request)
        status['nisponno_records']['note_nisponno'] = status_
        object = self.update_log(request, object=object, process_running=6, total_process=total_process)
        nisponno_records_objects = None
        nisponno_records_values = None
        nisponno_records_dataframe = None

        # Table 3: USERS
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
        object = self.update_log(request, object=object, process_running=7, total_process=total_process)

        # Table 4: USERS_EMPLOYEE_RECORDS
        status['users_employee_records'] = {}
        employee_records_objects = EmployeeRecords.objects.using('source_db').all()
        employee_records_values = employee_records_objects.values(
            'id', 'name_eng', 'gender', 'created', 'modified'
        )
        employee_records_dataframe = pd.DataFrame(employee_records_values)
        # male_female_users
        status_ = reports.male_female_nothi_users.update(
            request, users_dataframe, employee_records_dataframe
        )
        status['users_employee_records'] = status_
        object = self.update_log(request, object=object, process_running=8, total_process=total_process)

        users_objects = None
        users_values = None
        users_dataframe = None

        # Table 5: USER_LOGIN_HISTORY

        status['user_login_history'] = {}
        login_history_objects = UserLoginHistory.objects.using('source_db').all()
        login_history_values = login_history_objects.values(
            'id', 'is_mobile', 'created', 'employee_record_id', 'device_type'
        )
        login_history_dataframe = pd.DataFrame(login_history_values)
        # mobile_app_users
        status_ = reports.mobile_app_users.update(login_history_dataframe, request)
        status['user_login_history']['mobile_app_users'] = status_
        object = self.update_log(request, object=object, process_running=9, total_process=total_process)
        # Android-IOS users
        status_ = reports.android_ios_users.update(login_history_dataframe, request)
        status['user_login_history']['android_ios_users'] = status_
        object = self.update_log(request, object=object, process_running=10, total_process=total_process)
        # Login Total users
        status_ = reports.login_total_users.update(login_history_dataframe, request)
        status['user_login_history']['login_total_users'] = status_
        object = self.update_log(request, object=object, process_running=11, total_process=total_process)

        # Table 6: USER_LOGIN_HISTORY_EMPLOYEE_RECORDS
        # login_male_female_nothi_users
        status['user_login_history_employee_records'] = {}
        male_status, female_status = reports.login_male_female_users.update(
            request, login_history_dataframe, employee_records_dataframe
        )
        status['user_login_history_employee_records']['login_male_users'] = male_status
        object = self.update_log(request, object=object, process_running=12, total_process=total_process)
        status['user_login_history_employee_records'][
            'login_female_users'
        ] = female_status
        object = self.update_log(request, object=object, process_running=13, total_process=total_process)
        employee_records_objects = None
        employee_records_values = None
        employee_records_dataframe = None
        login_history_objects = None
        login_history_values = None
        login_history_dataframe = None

        settings.SYSTEM_UPDATE_RUNNING = False
        end_processing_time = time.perf_counter()
        status['computation_time'] = end_processing_time - start_processing_time

        object = self.update_log(request, object=object, process_running=None, total_process=total_process, status=status)

        return Response(status)
