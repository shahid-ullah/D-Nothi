# monthly_report/admin.py
from django.contrib import admin

from .models import (GeneralDrilldownJSONDataModel, MonthModel, ReportModel,
                     ReportTypeModel, YearModel)

admin.site.register(YearModel)
admin.site.register(MonthModel)
admin.site.register(ReportModel)
admin.site.register(ReportTypeModel)
admin.site.register(GeneralDrilldownJSONDataModel)
