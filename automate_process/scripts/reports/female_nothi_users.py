from automate_process.models import (EmployeeRecords, NisponnoRecords, Offices,
                                     UserLoginHistory, Users)
from backup_source_db.models import TrackBackupDBLastFetchTime

last_fetch_time_object = TrackBackupDBLastFetchTime.objects.using('backup_source_db').last()

def get_user_login_history_querysets(request, *args, **kwargs):
    try:
        last_fetch_time = last_fetch_time_object.user_login_history
    except AttributeError:
        breakpoint()
