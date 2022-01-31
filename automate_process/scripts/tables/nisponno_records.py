# Table Name: nisponno_records
# reports:
# Nispottikritto Nothi
# Total Upokarvogi
# Note Nisponno
# Potrojari

import json
import os

from django.conf import settings

from ...models import NisponnoRecords
from ..reports import (nispottikritto_nothi, note_nisponno, potrojari,
                       upokarvogi)


def update():
    objs = load_dataframe()

    nisponno_records = {}
    status = {}
    # update Nispottikritto nothi
    try:
        year_report = nispottikritto_nothi.update(objs)
        # year_report = mobile_app_users.update(objs)
        nisponno_records['nispottikritto_nothi'] = year_report
        status['nispottikritto_nothi'] = 'success'
    except Exception as e:
        nisponno_records['nispottikritto_nothi'] = []
        status['nispottikritto_nothi'] = 'Failed'
        print(e)

    # update upokarvogi
    try:
        year_report = upokarvogi.update(objs)
        nisponno_records['upokarvogi'] = year_report
        status['upokarvogi'] = 'success'
    except Exception as e:
        nisponno_records['upokarvogi'] = []
        status['upokarvogi'] = 'Failed'
        print(e)

    # update potrojari
    try:
        year_report = potrojari.update(objs)
        # year_report = mobile_app_users.update(objs)
        nisponno_records['potrojari'] = year_report
        status['potrojari'] = 'success'
    except Exception as e:
        nisponno_records['potrojari'] = []
        status['potrojari'] = 'Failed'
        print(e)

    # update note_nisponno
    try:
        year_report = upokarvogi.update(objs)
        # year_report = mobile_app_users.update(objs)
        nisponno_records['note_nisponno'] = year_report
        status['note_nisponno'] = 'success'
    except Exception as e:
        nisponno_records['note_nisponno'] = []
        status['note_nisponno'] = 'Failed'
        print(e)

    dir_name = 'temporary_data'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    path = dir_name + "/" + "nisponno_records.json"

    print(f"Saving graph data ...{path}")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nisponno_records, f, ensure_ascii=False, indent=4)

    return nisponno_records, status


def load_dataframe():
    if settings.DEBUG:
        objs = NisponnoRecords.objects.using('source_db').all()[:100000]
    else:
        objs = NisponnoRecords.objects.using('source_db').all()
    return objs
