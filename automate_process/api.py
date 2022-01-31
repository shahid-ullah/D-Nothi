import json

from django.conf import settings
from django.core.files.base import File
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from monthly_report.models import ReportStorageModel, TableNameModel

from .scripts.tables import offices, user_login_history


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
        try:
            status_ = user_login_history_table()
            status['user_login_history'] = status_

        except Exception as e:
            settings.SYSTEM_UPDATE_RUNNING = False
            return Response({'status': status, 'error': str(e)})

        try:
            status_ = offices_table()
            status['offices'] = status_

        except Exception as e:
            settings.SYSTEM_UPDATE_RUNNING = False
            return Response({'status': status, 'error': str(e)})

        settings.SYSTEM_UPDATE_RUNNING = False

        return Response(status)


def user_login_history_table():
    _, status = user_login_history.update()
    table_obj = TableNameModel.objects.filter(name='user_login_history').last()

    fd = open('temporary_data/user_login_history.json')
    f = File(fd)
    ReportStorageModel.objects.create(table_name=table_obj, file_name=f)
    f.close()
    fd.close()

    return status


def offices_table():
    _, status = offices.update()
    table_obj = TableNameModel.objects.filter(name='offices').last()

    fd = open('temporary_data/offices.json')
    f = File(fd)
    ReportStorageModel.objects.create(table_name=table_obj, file_name=f)
    f.close()
    fd.close()

    return status