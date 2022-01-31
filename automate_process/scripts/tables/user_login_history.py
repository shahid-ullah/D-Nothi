# Table Name: user_login_history
# Report1: mobile_app_users
# Report2: android_ios_users
import json
import os

from django.conf import settings

from ...models import UserLoginHistory
from ..reports import android_ios_users, mobile_app_users


def update():
    objs = load_dataframe()

    user_login_history = {}
    status = {}

    # update mobile app users
    try:
        year_report = mobile_app_users.update(objs)
        user_login_history['mobile_app_users'] = year_report
        status['mobile_app_users'] = 'success'
    except Exception as e:
        user_login_history['mobile_app_users'] = []
        status['mobile_app_users'] = 'Fails'
        print(e)

    # update Android-IOS users
    try:
        data = android_ios_users.update(objs)
        user_login_history['android_ios_users'] = data
        status['android_ios_users'] = 'success'
    except Exception as e:
        user_login_history['android_ios_users'] = []
        status['android_ios_users'] = 'Fails'
        print(e)

    dir_name = 'temporary_data'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    path = dir_name + "/" + "user_login_history.json"

    print(f"Saving graph data ...{path}")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(user_login_history, f, ensure_ascii=False, indent=4)
    return user_login_history, status


def load_dataframe():
    if settings.DEBUG:
        objs = UserLoginHistory.objects.using('source_db').all()[:100000]
    else:
        objs = UserLoginHistory.objects.using('source_db').all()
    return objs
