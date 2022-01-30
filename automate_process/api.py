from django.conf import settings
from django.core.files.base import File
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from monthly_report.models import (GeneralDrilldownJSONDataModel,
                                   ReportTypeModel)

from .scripts import mobile_app_users


class updateDashboard(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """

        if settings.SYSTEM_UPDATE_RUNNING:
            print('system update running. please request later')
            return Response({'status': 'system update running. Please request later'})

        settings.SYSTEM_UPDATE_RUNNING = True
        # updating mobile app users
        try:
            data = mobile_app_users.update()
            fd = open('temporary_data/mobile_app_users.json')
            f = File(fd)
            obj1 = ReportTypeModel.objects.filter(type_name='mobile_app_users').first()
            GeneralDrilldownJSONDataModel.objects.create(report_type=obj1, file_name=f)
            f.close()
            fd.close()
        except Exception as e:
            settings.SYSTEM_UPDATE_RUNNING = False
            return Response({'error': str(e)})

        settings.SYSTEM_UPDATE_RUNNING = False
        return Response(data)
