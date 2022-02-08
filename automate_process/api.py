# import json

from django.conf import settings
# from django.core.files.base import File
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .scripts.tables import (nisponno_records, offices, user_login_history,
                             users, users_employee_records)

# from monthly_report.models import ReportStorageModel, TableNameModel


class updateDashboard(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
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
        # try:
        #     status_ = user_login_history_table()
        #     status['user_login_history'] = status_

        # except Exception as e:
        #     # settings.SYSTEM_UPDATE_RUNNING = False
        #     # return Response({'status': status, 'error': str(e)})
        #     print(e)

        try:
            offices_status = offices_table(request)
            status['offices'] = offices_status

        except Exception as e:
            # settings.SYSTEM_UPDATE_RUNNING = False
            # return Response({'status': status, 'error': str(e)})
            print(e)

        # try:
        #     status_ = nisponno_records_table(request)
        #     status['nisponno_records'] = status_

        # except Exception as e:
        #     # settings.SYSTEM_UPDATE_RUNNING = False
        #     # return Response({'status': status, 'error': str(e)})
        #     print(e)

        # try:
        #     status_ = users_table(request)
        #     status['users'] = status_

        # except Exception as e:
        #     # settings.SYSTEM_UPDATE_RUNNING = False
        #     # return Response({'status': status, 'error': str(e)})
        #     print(e)

        # try:
        #     status_ = users_employee_records_table(request)
        #     status['users_employee_records'] = status_

        # except Exception as e:
        #     # settings.SYSTEM_UPDATE_RUNNING = False
        #     # return Response({'status': status, 'error': str(e)})
        #     print(e)

        settings.SYSTEM_UPDATE_RUNNING = False

        return Response(status)


def user_login_history_table():
    _, status = user_login_history.update()

    return status


def offices_table(request=None, *args, **kwargs):
    offices_status = offices.update(request)

    return offices_status


def nisponno_records_table(request=None, *args, **kwargs):
    _, status = nisponno_records.update(request)

    return status


def users_table(request=None):
    _, status = users.update(request)

    return status


def users_employee_records_table(request=None):
    _, status = users_employee_records.update(request)

    return status
