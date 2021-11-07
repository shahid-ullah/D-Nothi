# monthly_report/admin.py
from django.contrib import admin

from .models import MonthModel, ReportModel, YearModel

admin.site.register(YearModel)
admin.site.register(MonthModel)
admin.site.register(ReportModel)
