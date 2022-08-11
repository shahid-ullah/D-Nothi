from django.contrib import admin

from .models import (BackupEmployeeRecords, BackupNisponnoRecords,
                     BackupOffices, BackupUserLoginHistory, BackupUsers)

admin.site.register(BackupOffices)
admin.site.register(BackupUsers)
admin.site.register(BackupEmployeeRecords)
admin.site.register(BackupNisponnoRecords)
admin.site.register(BackupUserLoginHistory)
