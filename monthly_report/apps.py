import os

import pandas as pd
from django.apps import AppConfig
from django.conf import settings

# from .models import YearModel


class MonthlyReportConfig(AppConfig):
    name = 'monthly_report'
    # from .models import YearModel

    offices_file_path = os.path.join(settings.DATA_BASE_DIR_PATH, 'offices.csv')
    offices_df = pd.read_csv(offices_file_path)
    # print('APP config')
    # print()
    # print(offices_df[:5])
    # obj = YearModel.objects.last()
    # print('object: ', obj)
