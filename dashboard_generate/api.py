# dashboard_generate/api.py
import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView

from automate_process.models import (EmployeeRecords, NisponnoRecords, Offices,
                                     UserLoginHistory, Users)

from .models import (ReportAndroidUsersModel, ReportFemaleNothiUsersModel,
                     ReportIOSUsersModel, ReportLoginFemalelUsersModel,
                     ReportLoginMalelUsersModel, ReportLoginTotalUsers,
                     ReportMaleNothiUsersModel, ReportMobileAppUsersModel,
                     ReportNispottikrittoNothiModel, ReportNoteNisponnoModel,
                     ReportPotrojariModel, ReportTotalOfficesModel,
                     ReportTotalUsersModel, ReportUpokarvogiModel)


class SourceDBStatusAPI(APIView):
    def get(self, request, format=None):
        """ """

        try:
            status = generate_status(request)
        except Exception as e:
            status = {}
            print(e)

        return Response(status)


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

    model_list1 = [EmployeeRecords, Offices, UserLoginHistory, Users]
    model_list2 = [NisponnoRecords]
    # model_list1 = [Offices]
    # model_list2 = [NisponnoRecords]
    status = {}
    for model in model_list1:
        objs = model.objects.using('source_db').all()
        values = objs.values(
            'created',
        )
        dataframe = pd.DataFrame(values)
        status.setdefault(model.__name__, {})
        status[model.__name__]['table_size'] = dataframe.shape[0]
        status[model.__name__][
            'report_date_range'
        ] = f'{dataframe.created.min()} - {dataframe.created.max()}'

    for model in model_list2:
        objs = model.objects.using('source_db').all()
        values = objs.values(
            'operation_date',
        )
        dataframe = pd.DataFrame(values)
        status.setdefault(model.__name__, {})
        status[model.__name__]['table_size'] = dataframe.shape[0]
        status[model.__name__][
            'report_date_range'
        ] = f'{dataframe.operation_date.min()} - {dataframe.operation_date.max()}'

        return status
