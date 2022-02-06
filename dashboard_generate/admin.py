from django.contrib import admin

# Register your models here.
from .models import ReportTotalOfficesModel


@admin.register(ReportTotalOfficesModel)
class PostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReportTotalOfficesModel._meta.get_fields()]
