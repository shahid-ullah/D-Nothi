# Total Offices

from django.conf import settings

from ...models import Offices
from ..reports import total_offices


def update(request=None, *args, **kwargs):
    objs = load_dataframe()
    offices_status = {}
    total_offices_status = {}

    try:
        last_report_date = total_offices.update(objs, request, *args, **kwargs)
        total_offices_status['last_report_date'] = str(last_report_date)
        total_offices_status['status'] = 'success'
    except Exception as e:
        total_offices_status['status'] = 'Failed'
        total_offices_status['last_report_date'] = []
        print(e)
        print()

    offices_status['total_offices'] = total_offices_status

    return offices_status


def load_dataframe():
    if settings.DEBUG:
        objs = Offices.objects.using('source_db').all()[:1000]
    else:
        query = settings.QUERY_CREATED_DATE
        objs = Offices.objects.using('source_db').filter(query)

    return objs
