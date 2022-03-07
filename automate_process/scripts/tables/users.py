# Table Name: users
# Report 1: total_nothi_users


from django.conf import settings

from ...models import Users
from ..reports import total_nothi_users


def update(request=None, *args, **kwargs):
    objs = load_dataframe()

    users_status = {}
    total_nothi_users_status = {}

    # total_nothi_users
    try:
        last_report_date = total_nothi_users.update(objs, request)
        total_nothi_users_status['last_report_date'] = str(last_report_date)
        total_nothi_users_status['status'] = 'success'
    except Exception as e:
        total_nothi_users_status['last_report_date'] = []
        total_nothi_users_status['status'] = 'Failed'
        print(e)

    users_status['total_nothi_users'] = total_nothi_users_status

    return users_status


def load_dataframe():
    if settings.DEBUG:
        objs = Users.objects.using('source_db').all()[:1000]
    else:
        query = settings.QUERY_CREATED_DATE
        objs = Users.objects.using('source_db').filter(query)

    return objs
