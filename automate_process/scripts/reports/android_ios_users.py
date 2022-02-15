# scripts/reports/android_ios_users.py

import pandas as pd

from dashboard_generate.models import (ReportAndroidUsersModel,
                                       ReportIOSUsersModel)

from ..utils import utilsContainer


def update(objs, request=None, *args, **kwargs):
    utilsObject = utilsContainer()
    print()
    print('start processing android & ios users report')

    values = objs.values('id', 'is_mobile', 'device_type', 'created')
    dataframe = pd.DataFrame(values)

    dataframe = dataframe.loc[dataframe.is_mobile == 1]
    # remove null values
    # dataframe = dataframe.loc[dataframe.created.notnull()]
    dataframe['created'] = dataframe.created.fillna(method='bfill')

    android_dataframe = dataframe.loc[dataframe.device_type == 'android']
    android_groupby_date = android_dataframe.groupby(android_dataframe.created.dt.date)
    android_last_report_date = utilsObject.format_and_load_to_mysql_db(
        request, android_groupby_date, ReportAndroidUsersModel
    )

    ios_dataframe = dataframe.loc[dataframe.device_type == 'IOS']
    ios_groupby_date = ios_dataframe.groupby(ios_dataframe.created.dt.date)
    ios_last_report_date = utilsObject.format_and_load_to_mysql_db(
        request, ios_groupby_date, ReportIOSUsersModel
    )

    print()
    print('End processing android & ios users report')

    return android_last_report_date, ios_last_report_date
