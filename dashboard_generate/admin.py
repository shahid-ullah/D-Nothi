from django.contrib import admin

# Register your models here.
from .models import (ReportAndroidUsersModel, ReportFemaleNothiUsersModel,
                     ReportIOSUsersModel, ReportLoginTotalUsers,
                     ReportMaleNothiUsersModel, ReportMobileAppUsersModel,
                     ReportNispottikrittoNothiModel, ReportNoteNisponnoModel,
                     ReportPotrojariModel, ReportTotalOfficesModel,
                     ReportTotalUsersModel, ReportUpokarvogiModel)


@admin.register(ReportTotalOfficesModel)
class ReportTotalOfficeModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReportTotalOfficesModel._meta.get_fields()]


@admin.register(ReportNispottikrittoNothiModel)
class ReportNispottikrittoNothiModelAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in ReportNispottikrittoNothiModel._meta.get_fields()
    ]


@admin.register(ReportUpokarvogiModel)
class ReportUpokarvogiAmdin(admin.ModelAdmin):
    list_display = [field.name for field in ReportUpokarvogiModel._meta.get_fields()]


@admin.register(ReportPotrojariModel)
class ReportPotrojariModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReportPotrojariModel._meta.get_fields()]


@admin.register(ReportNoteNisponnoModel)
class ReportNoteNisponnoModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReportNoteNisponnoModel._meta.get_fields()]


@admin.register(ReportTotalUsersModel)
class ReportTotalUsersModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReportTotalUsersModel._meta.get_fields()]


@admin.register(ReportMaleNothiUsersModel)
class ReportMaleNothiUsersModelAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in ReportMaleNothiUsersModel._meta.get_fields()
    ]


@admin.register(ReportFemaleNothiUsersModel)
class ReportFemaleNothiUsersModelAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in ReportFemaleNothiUsersModel._meta.get_fields()
    ]


@admin.register(ReportMobileAppUsersModel)
class ReportMobileAppUsersModelAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in ReportMobileAppUsersModel._meta.get_fields()
    ]


@admin.register(ReportAndroidUsersModel)
class ReportAndroidUsersModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReportAndroidUsersModel._meta.get_fields()]


@admin.register(ReportIOSUsersModel)
class ReportIOSUsersModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReportIOSUsersModel._meta.get_fields()]


@admin.register(ReportLoginTotalUsers)
class ReportLoginTotalUsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'year', 'month', 'day', 'count_or_sum']
