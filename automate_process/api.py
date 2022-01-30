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
        fd = open('temporary_data/mobile_app_users.json')
        f = File(fd)
        data = mobile_app_users.update()
        obj1 = ReportTypeModel.objects.filter(type_name='mobile_app_users').first()
        GeneralDrilldownJSONDataModel.objects.create(report_type=obj1, file_name=f)
        f.close()
        fd.close()
        return Response(data)
