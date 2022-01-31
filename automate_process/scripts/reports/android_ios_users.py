# scripts/reports/android_ios_users.py
import pandas as pd


def update(objs, *args, **kwargs):

    values = objs.values('id', 'is_mobile', 'device_type', 'created')
    dataframe = pd.DataFrame(values)

    android_ios_users = dataframe.loc[
        (dataframe.device_type == 'android') | (dataframe.device_type == 'IOS')
    ]['device_type'].value_counts()

    data = []
    for item in android_ios_users.iteritems():
        dic = {str(item[0]): item[1]}
        data.append(dic)

    return data
