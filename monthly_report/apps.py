import os

import pandas as pd
from django.apps import AppConfig
from django.conf import settings

# from .models import YearModel


class MonthlyReportConfig(AppConfig):
    name = 'monthly_report'
