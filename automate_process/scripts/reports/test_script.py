# scripts/reports/test_script.py
import pandas as pd

from automate_process.models import (EmployeeRecords, NisponnoRecords, Offices,
                                     UserLoginHistory)
from dashboard_generate.models import ReportTotalOfficesModel

# target: get day, count map of source db and dashboad db
# and compare the count

source_db_models = ['EmployeeRecords', 'Offices', 'NisponnoRecords', 'UserLoginHistory']
source_offices_map = {}
source_employee_records_map = {}
source_nisponno_records_map = {}
source_user_login_history_map = {}

destination_db_models = []


dashboard_objects = ReportTotalOfficesModel.objects.all()
dashboard_values = dashboard_objects.values('year_month_day', 'count_or_sum')
dashboard_db_map = {}
for object in dashboard_values:
    dashboard_db_map[object['year_month_day']] = object['count_or_sum']
# print(dashboard_map)
source_db_map = {}
values = Offices.objects.using('source_db').filter(active_status=1).values('created')
dataframe = pd.DataFrame(values)
dataframe['created'] = dataframe.created.fillna(method='bfill')
groupby_date = dataframe.groupby(dataframe.created.dt.date)
for gr, fr in groupby_date:
    source_db_map[str(gr).replace('-', '')] = int(fr.shape[0])
for key, value in source_db_map.items():
    if not dashboard_db_map[key] == value:
        print('Error')
