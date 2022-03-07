# dashboard_generate/api.py
import time

import pandas as pd
from rest_framework import authentication, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from automate_process.models import (EmployeeRecords, NisponnoRecords, Offices,
                                     UserLoginHistory, Users)

from .models import (DashboardUpdateLog, ReportAndroidUsersModel,
                     ReportFemaleNothiUsersModel, ReportIOSUsersModel,
                     ReportLoginFemalelUsersModel, ReportLoginMalelUsersModel,
                     ReportLoginTotalUsers, ReportMaleNothiUsersModel,
                     ReportMobileAppUsersModel, ReportNispottikrittoNothiModel,
                     ReportNoteNisponnoModel, ReportPotrojariModel,
                     ReportTotalOfficesModel, ReportTotalUsersModel,
                     ReportUpokarvogiModel)
from .serializers import DashboardUpdateLogSerializer


class SourceDBStatusAPI(APIView):
    def get(self, request, format=None):
        """ """

        try:
            status = generate_status(request)
        except Exception as e:
            status = {'error': str(e)}
            print(e)

        return Response(status)


class DashboardUpdateLogAPI(generics.ListAPIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = DashboardUpdateLog.objects.all()
    serializer_class = DashboardUpdateLogSerializer


class ReportDBStatus(APIView):
    def get(self, request, format=None):
        """ """

        models = [
            ReportAndroidUsersModel,
            ReportFemaleNothiUsersModel,
            ReportIOSUsersModel,
            ReportLoginFemalelUsersModel,
            ReportLoginMalelUsersModel,
            ReportLoginTotalUsers,
            ReportMaleNothiUsersModel,
            ReportMobileAppUsersModel,
            ReportNispottikrittoNothiModel,
            ReportNoteNisponnoModel,
            ReportPotrojariModel,
            ReportTotalOfficesModel,
            ReportTotalUsersModel,
            ReportUpokarvogiModel,
        ]

        status = {}
        for model in models:
            try:
                objs = model.objects.all()
                values = objs.values(
                    'report_day',
                )
                dataframe = pd.DataFrame(values)
                status.setdefault(model.__name__, {})
                status[model.__name__]['table_size'] = dataframe.shape[0]
                status[model.__name__][
                    'report_date_range'
                ] = f'{dataframe.report_day.min()} - {dataframe.report_day.max()}'
            except Exception as e:
                status[model.__name__] = str(e)
                print(e)

        return Response(status)


def generate_status(request, *args, **kwargs):

    start = time.perf_counter()

    model_list1 = [EmployeeRecords, Offices, UserLoginHistory, Users, NisponnoRecords]
    status = {}
    for model in model_list1:
        objs = model.objects.using('source_db').all()

        first_object = objs.first()
        last_object = objs.last()

        report_first_date = get_report_first_date(
            objs, first_object.id, first_object.created
        )
        report_last_date = get_report_last_date(
            objs, last_object.id, last_object.created
        )

        status.setdefault(model.__name__, {})
        status[model.__name__]['table_size'] = objs.count()
        status[model.__name__][
            'report_date_range'
        ] = f"{report_last_date} - {report_first_date}"

    stop = time.perf_counter()
    status['coputation_time'] = stop - start

    return status


def get_report_first_date(objs, id, report_time):
    if report_time:
        return report_time

    id = id + 1
    try:

        obj = objs[id]
        id = obj.id
        report_time = obj.created
    except IndexError:
        id = id + 1

    return get_report_first_date(objs, id, report_time)


def get_report_last_date(objs, id, report_time):
    if report_time:
        return report_time

    id = id - 1
    try:

        obj = objs[id]
        id = obj.id
        report_time = obj.created
    except IndexError:
        id = id - 1

    return get_report_last_date(objs, id, report_time)
