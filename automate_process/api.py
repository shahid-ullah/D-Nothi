# import json

from django.conf import settings
# from django.core.files.base import File
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .scripts.tables import (nisponno_records, offices, user_login_history,
                             user_login_history_employee_records, users,
                             users_employee_records)


class updateDashboard(APIView):
    """
    update dashboard data.
    process source db data and dump to dashboard db.
    """

    authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """ """

        status = {}
        if settings.SYSTEM_UPDATE_RUNNING:
            print('system update running. please request later')
            return Response({'status': 'system update running. Please request later'})

        settings.SYSTEM_UPDATE_RUNNING = True

        # Table 1: offices
        try:
            offices_status = offices_table(request)
            status['offices'] = offices_status

        except Exception as e:
            print(e)

        # Table 2: nisponno_records
        try:
            nisponno_records_status = nisponno_records_table(request)
            status['nisponno_records'] = nisponno_records_status
        except Exception as e:
            print(e)

        # Table 3: users
        try:
            users_status = users_table(request)
            status['users'] = users_status

        except Exception as e:
            print(e)

        # Table 4: users_employee_records
        try:
            users_emploee_records_status = users_employee_records_table(request)
            status['users_employee_records'] = users_emploee_records_status

        except Exception as e:
            print(e)

        # Table 5: user_login_history
        try:
            status_ = user_login_history_table(request)
            status['user_login_history'] = status_

        except Exception as e:
            print(e)

        # Table 6: user_login_history_employee_records
        try:
            status_ = user_login_history_employee_records_table(request)
            status['user_login_history_employee_records'] = status_

        except Exception as e:
            print(e)

        settings.SYSTEM_UPDATE_RUNNING = False

        return Response(status)


def user_login_history_table(request=None, *args, **kwargs):
    user_login_history_status = user_login_history.update(request, *args, **kwargs)

    return user_login_history_status


def offices_table(request=None, *args, **kwargs):
    offices_status = offices.update(request)

    return offices_status


def nisponno_records_table(request=None, *args, **kwargs):
    nisponno_records_status = nisponno_records.update(request)

    return nisponno_records_status


def users_table(request=None):
    users_status = users.update(request)

    return users_status


def users_employee_records_table(request=None):
    users_employee_records_status = users_employee_records.update(request)

    return users_employee_records_status


def user_login_history_employee_records_table(request=None):
    users_employee_records_status = user_login_history_employee_records.update(request)

    return users_employee_records_status
