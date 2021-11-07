# monthly_report/utils.py

import pandas as pd
from django.conf import settings

from .models import CSVDataStorageModel, TableNameModel


def load_csv(table_name=None):
    csv_data = CSVDataStorageModel.objects.filter(table_name=table_name).last()
    settings.OFFICES_CSV_FILE_PATH = pd.read_csv(csv_data.file_name.path)
    settings.OFFICES_CSV_FILE_LOADED = True


def load_office_table():
    table = TableNameModel.objects.filter(name='offices').last()
    load_csv(table)
