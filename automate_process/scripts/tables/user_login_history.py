# Table Name: user_login_history
# Report1: mobile_app_users
# Report2: android_ios_users
# Report3: Total Users (login)

from django.conf import settings

from ...models import UserLoginHistory
from ..reports import android_ios_users, login_total_users, mobile_app_users


def update(request=None, *args, **kwargs):
    objs = load_dataframe()

    user_login_history_status = {}
    mobile_app_users_status = {}
    android_ios_users_status = {}
    login_total_users_status = {}

    # mobile app users
    try:
        last_report_date = mobile_app_users.update(objs, request, *args, **kwargs)
        mobile_app_users_status['last_report_date'] = str(last_report_date)
        mobile_app_users_status['status'] = 'success' ''
    except Exception as e:
        mobile_app_users_status['last_report_date'] = ''
        mobile_app_users_status['status'] = 'Failed'
        print(e)

    # Android-IOS users
    try:
        android_last_report_date, ios_last_report_date = android_ios_users.update(
            objs, request, *args, **kwargs
        )
        android_ios_users_status['last_report_date'] = {
            'android': str(android_last_report_date),
            'ios': str(ios_last_report_date),
        }
        android_ios_users_status['status'] = 'success'
    except Exception as e:
        android_ios_users_status['last_report_date'] = {
            'android': '',
            'ios': '',
        }
        android_ios_users_status['status'] = 'Failed'
        print(e)
    # Login Total Users
    try:
        last_report_date = login_total_users.update(objs, request, *args, **kwargs)
        login_total_users_status['last_report_date'] = str(last_report_date)
        android_ios_users_status['status'] = 'success'
    except Exception as e:
        login_total_users_status['last_report_date'] = ''
        login_total_users_status['status'] = 'Failed'
        print(e)

    user_login_history_status['mobile_app_users'] = mobile_app_users_status
    user_login_history_status['android_ios_users'] = android_ios_users_status
    user_login_history_status['login_total_users'] = login_total_users_status

    return user_login_history_status


def load_dataframe():
    if settings.DEBUG:
        objs = UserLoginHistory.objects.using('source_db').all()[:1000]
    else:
        objs = UserLoginHistory.objects.using('source_db').all()
    return objs
