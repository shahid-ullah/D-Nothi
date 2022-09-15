from django.contrib import admin

from automate_process.models import (
    EmployeeRecords,
    NisponnoRecords,
    Offices,
    SourceDBLog,
    TrackSourceDBLastFetchTime,
    UserLoginHistory,
    Users,
)


@admin.register(EmployeeRecords)
class EmployeeRecordsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EmployeeRecords._meta.get_fields()]


@admin.register(Offices)
class OfficesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Offices._meta.get_fields()]


@admin.register(UserLoginHistory)
class UserLoginHistoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserLoginHistory._meta.get_fields()]


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Users._meta.get_fields()]


@admin.register(NisponnoRecords)
class NisponnoRecordsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NisponnoRecords._meta.get_fields()]


@admin.register(TrackSourceDBLastFetchTime)
class TrackSourceDBLastFetchTimeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TrackSourceDBLastFetchTime._meta.get_fields()]


@admin.register(SourceDBLog)
class SourceDBLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SourceDBLog._meta.get_fields()]
