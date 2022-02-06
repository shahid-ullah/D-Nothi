from django.contrib import admin

# Register your models here.
from .models import (ReportNispottikrittoNothiModel, ReportTotalOfficesModel,
                     ReportUpokarvogiModel)


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
