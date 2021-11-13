# monthly_report/admin.py
from django.contrib import admin

from .models import (CSVDataStorageModel, DataframeRecord, MonthModel,
                     ReportModel, YearModel)

admin.site.register(DataframeRecord)
admin.site.register(CSVDataStorageModel)
admin.site.register(YearModel)
admin.site.register(MonthModel)
admin.site.register(ReportModel)
