# Table Name: nisponno_records
# reports:
# Nispottikritto Nothi
# Total Upokarvogi
# Note Nisponno
# Potrojari

# import json
# import os

# from django.conf import settings

from ...models import NisponnoRecords
from ..reports import (nispottikritto_nothi, note_nisponno, potrojari,
                       upokarvogi)


def update(request=None, *args, **kwargs):
    objs = load_dataframe()

    nisponno_records_status = {}
    nispottikritto_nothi_status = {}
    upokarvogi_status = {}

    # Nispottikritto nothi
    try:
        last_report_date = nispottikritto_nothi.update(objs, request, *args, **kwargs)
        nispottikritto_nothi_status['last_report_date'] = str(last_report_date)
        nispottikritto_nothi_status['status'] = 'success'
    except Exception as e:
        nispottikritto_nothi_status['last_report_date'] = []
        nispottikritto_nothi_status['status'] = 'Failed'
        print(e)

    # upokarvogi
    # try:
    #     last_report_date = upokarvogi.update(objs, request, *args, **kwargs)
    #     upokarvogi_status['last_report_date'] = last_report_date
    #     upokarvogi_status['status'] = 'success'
    # except Exception as e:
    #     upokarvogi_status['last_report_date'] = []
    #     upokarvogi_status['status'] = 'Failed'
    #     print(e)

    # update potrojari
    # try:
    #     year_report = potrojari.update(objs, request, *args, **kwargs)
    #     # year_report = mobile_app_users.update(objs)
    #     nisponno_records['potrojari'] = year_report
    #     status['potrojari'] = 'success'
    # except Exception as e:
    #     nisponno_records['potrojari'] = []
    #     status['potrojari'] = 'Failed'
    #     print(e)

    # update note_nisponno
    # try:
    #     year_report = note_nisponno.update(objs, request, *args, **kwargs)
    #     # year_report = mobile_app_users.update(objs)
    #     nisponno_records['note_nisponno'] = year_report
    #     status['note_nisponno'] = 'success'
    # except Exception as e:
    #     nisponno_records['note_nisponno'] = []
    #     status['note_nisponno'] = 'Failed'
    #     print(e)
    nisponno_records_status['nispottikritto_nothi'] = nispottikritto_nothi_status

    return nisponno_records_status


def load_dataframe():
    objs = NisponnoRecords.objects.using('source_db').all()

    return objs
