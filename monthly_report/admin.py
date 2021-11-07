# monthly_report/admin.py
from django.contrib import admin

from .models import (CSVDataStorageModel, MonthModel, ReportModel,
                     TableNameModel, YearModel)

admin.site.register(TableNameModel)
admin.site.register(CSVDataStorageModel)
admin.site.register(YearModel)
admin.site.register(MonthModel)
admin.site.register(ReportModel)
