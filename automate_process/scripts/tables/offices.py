# Total Offices
import json
import os

from django.conf import settings

from ...models import Offices
from ..reports import total_offices


def update(request=None, *args, **kwargs):
    # print(request.user)
    # breakpoint()
    objs = load_dataframe()
    offices = {}
    status = {}

    try:
        year_report = total_offices.update(objs, request, *args, **kwargs)
        offices['total_offices'] = year_report
        status['total_offices'] = 'success'
    except Exception as e:
        offices['total_offices'] = []
        status['total_offices'] = 'Failed'
        print(e)
        print()

    # dir_name = 'temporary_data'
    # if not os.path.exists(dir_name):
    #     os.makedirs(dir_name)

    # path = dir_name + "/" + "offices.json"

    # print(f"Saving graph data ...{path}")
    # with open(path, 'w', encoding='utf-8') as f:
    #     json.dump(offices, f, ensure_ascii=False, indent=4)

    return offices, status


def load_dataframe():
    if settings.DEBUG:
        objs = Offices.objects.using('source_db').all()[:100000]
    else:
        objs = Offices.objects.using('source_db').all()
    return objs
