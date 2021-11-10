# monthly_report/utils.py

import pandas as pd
from django.conf import settings

from .models import CSVDataStorageModel, TableNameModel


def load_csv(table_name=None):
    csv_data = CSVDataStorageModel.objects.filter(table_name=table_name).first()
    path = pd.read_csv(csv_data.file_name.path)
    return path


def load_office_table():
    if not settings.OFFICES_CSV_FILE_LOADED:
        print('loading office table data')
        table = TableNameModel.objects.filter(name='offices').first()
        path = load_csv(table)
        settings.OFFICES_CSV_FILE_PATH = path
        settings.OFFICES_CSV_FILE_LOADED = True


def load_nisponno_records_table():
    if not settings.NISPONNO_RECORDS_CSV_FILE_LOADED:
        print('loading nisponno_records table data')
        table = TableNameModel.objects.filter(name='nisponno_records').first()
        path = load_csv(table)
        settings.NISPONNO_RECORDS_CSV_FILE_PATH = path
        settings.NISPONNO_RECORDS_CSV_FILE_LOADED = True


def load_users_table():
    if not settings.USERS_TABLE_CSV_FILE_LOADED:
        print('loading users table data')
        table = TableNameModel.objects.filter(name='users').first()
        path = load_csv(table)
        settings.USERS_TABLE_CSV_FILE_PATH = path
        settings.USERS_TABLE_CSV_FILE_LOADED = True


def load_users_gender_male_table():
    if not settings.USERS_GENDER_MALE_TABLE_CSV_FILE_LOADED:
        print('loading users table data')
        table = TableNameModel.objects.filter(name='users_gender_male').first()
        path = load_csv(table)
        settings.USERS_GENDER_MALE_TABLE_CSV_FILE_PATH = path
        settings.USERS_GENDER_MALE_TABLE_CSV_FILE_LOADED = True
