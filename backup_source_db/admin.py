from django.contrib import admin

from .models import (
    BackupDBLog,
    BackupEmployeeRecords,
    BackupNisponnoRecords,
    BackupOffices,
    BackupUserLoginHistory,
    BackupUsers,
)


@admin.register(BackupOffices)
class BackupOfficesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BackupOffices._meta.get_fields()]


@admin.register(BackupUsers)
class BackupUsersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BackupUsers._meta.get_fields()]


@admin.register(BackupEmployeeRecords)
class BackupEmployeeRecordsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BackupEmployeeRecords._meta.get_fields()]


@admin.register(BackupNisponnoRecords)
class BackupNisponnoRecordsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BackupNisponnoRecords._meta.get_fields()]


@admin.register(BackupUserLoginHistory)
class BackupUserLoginHistoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BackupUserLoginHistory._meta.get_fields()]


@admin.register(BackupDBLog)
class BackupDBLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BackupDBLog._meta.get_fields()]
