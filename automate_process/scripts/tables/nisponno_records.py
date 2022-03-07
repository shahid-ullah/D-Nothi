# Table Name: nisponno_records
# reports:
# Nispottikritto Nothi
# Total Upokarvogi
# Note Nisponno
# Potrojari

# import json
# import os

from django.conf import settings

from ...models import NisponnoRecords
from ..reports import (nispottikritto_nothi, note_nisponno, potrojari,
                       upokarvogi)


def update(request=None, *args, **kwargs):
    objs = load_dataframe()

    nisponno_records_status = {}
    nispottikritto_nothi_status = {}
    upokarvogi_status = {}
    potrojari_status = {}
    note_nisponno_status = {}

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
    try:
        last_report_date = upokarvogi.update(objs, request, *args, **kwargs)
        upokarvogi_status['last_report_date'] = str(last_report_date)
        upokarvogi_status['status'] = 'success'
    except Exception as e:
        upokarvogi_status['last_report_date'] = []
        upokarvogi_status['status'] = 'Failed'
        print(e)

    # potrojari
    try:
        last_report_date = potrojari.update(objs, request, *args, **kwargs)
        # year_report = mobile_app_users.update(objs)
        potrojari_status['last_report_date'] = str(last_report_date)
        potrojari_status['status'] = 'success'
    except Exception as e:
        potrojari_status['potrojari'] = []
        potrojari_status['status'] = 'Failed'
        print(e)

    # note_nisponno
    try:
        last_report_date = note_nisponno.update(objs, request, *args, **kwargs)
        # year_report = mobile_app_users.update(objs)
        note_nisponno_status['last_report_date'] = str(last_report_date)
        note_nisponno_status['status'] = 'success'
    except Exception as e:
        note_nisponno_status['potrojari'] = []
        note_nisponno_status['status'] = 'Failed'
        print(e)

    nisponno_records_status['nispottikritto_nothi'] = nispottikritto_nothi_status
    nisponno_records_status['upokarvogi'] = upokarvogi_status
    nisponno_records_status['potrojari'] = potrojari_status
    nisponno_records_status['note_nisponno'] = note_nisponno_status

    return nisponno_records_status


def load_dataframe():
    if settings.DEBUG:
        objs = NisponnoRecords.objects.using('source_db').all()[:1000]
    else:
        objs = NisponnoRecords.objects.using('source_db').all()

    return objs
