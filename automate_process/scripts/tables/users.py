# Table Name: users
# Report 1: total_nothi_users

import json
import os

from django.conf import settings

from ...models import Users
from ..reports import total_nothi_users


def update():
    objs = load_dataframe()

    users = {}
    status = {}
    # update total_nothi_users
    try:
        year_report = total_nothi_users.update(objs)
        # year_report = mobile_app_users.update(objs)
        users['total_nothi_users'] = year_report
        status['total_nothi_users'] = 'success'
    except Exception as e:
        users['total_nothi_users'] = []
        status['total_nothi_users'] = 'Failed'
        print(e)

    dir_name = 'temporary_data'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    path = dir_name + "/" + "users.json"

    print(f"Saving graph data ...{path}")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

    return users, status


def load_dataframe():
    if settings.DEBUG:
        objs = Users.objects.using('source_db').all()[:100000]
    else:
        objs = Users.objects.using('source_db').all()
    return objs
