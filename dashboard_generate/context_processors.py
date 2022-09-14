import datetime

from backup_source_db.models import BackupDBLog


def get_last_dashboard_update_time(request):
    current_datetime = datetime.datetime.now()
    last_object = BackupDBLog.objects.using('backup_source_db').last()
    last_update_time = None
    try:
        last_update_time = last_object.created
    except:
        pass

    return {'last_update': last_update_time}
