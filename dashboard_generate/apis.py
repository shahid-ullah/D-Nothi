# dashboard_generate/api.py

from os import wait

from django.db.models import Sum
from django_redis import get_redis_connection
from rest_framework import authentication, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DashboardUpdateLog, ReportLoginTotalUsersNotDistinct
from .serializers import DashboardUpdateLogSerializer


class DashboardUpdateLogAPI(generics.ListAPIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = DashboardUpdateLog.objects.all()
    serializer_class = DashboardUpdateLogSerializer


class LoginUsersNotDistinctAPI(APIView):

    # authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        office_ids = request.GET.get('office_ids')
        if office_ids:
            office_ids = office_ids.strip(', ').split(',')
            office_ids = [int(office_id) for office_id in office_ids]
            querysets = ReportLoginTotalUsersNotDistinct.objects.filter(office_id__in=office_ids)
            total_users_counts = querysets.aggregate(Sum('counts'))
            total_users = total_users_counts['counts__sum']
            if not total_users:
                total_users = 0
            response = {'office_ids': office_ids, 'counts': total_users}
            return Response(response)

        querysets = ReportLoginTotalUsersNotDistinct.objects.all()
        total_users_counts = querysets.aggregate(Sum('counts'))
        total_users = total_users_counts['counts__sum']
        response = {'office_ids': None, 'counts': total_users}
        return Response(response)


class ClearCacheAPI(APIView):

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        redis_instance = get_redis_connection('default')
        response = {}

        try:
            redis_instance.flushdb()
            response = {'status': 'success'}
        except Exception as e:
            print(e)
            response = {
                'status': 'failed',
                'error': str(e),
            }

        return Response(response)
