# Total Offices

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
    objs = Offices.objects.using('source_db').all()

    return objs
