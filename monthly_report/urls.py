# /src/clinic/urls.py

from datetime import datetime

import django.contrib.auth.views
from django.conf.urls import url
from django.urls import path, re_path

from . import views
from .api import ReportListAPI

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('report/', ReportListAPI.as_view(), name='report'),
    path('report/<query_year>/', ReportListAPI.as_view(), name='report'),
    #     # path('report/edit/', reportEdit, name='report_edit'),
    #     # path('report/new/', new_report, name='new_report'),
    #     # Nothi section
    #     path(
    #         'nispottikritto_nothi_yearwise/',
    #         views.nispottikritto_nothi_yearwise,
    #         name="nispottikritto_nothi_yearwise",
    #     ),
    path(
        'nispottikritto_nothi/',
        views.nispottikritto_nothi,
        name="nispottikritto_nothi",
    ),
    #     path(
    #         'nothi_users_total/',
    #         views.nothi_users_total,
    #         name="nothi_users_total",
    #     ),
    path(
        'nothi_users_male/',
        views.nothi_users_male,
        name="nothi_users_male",
    ),
    #     path(
    #         'nothi_users_female/',
    #         views.nothi_users_female,
    #         name="nothi_users_female",
    #     ),
    #     path(
    #         'mobile_app_users/',
    #         views.mobile_app_users,
    #         name="mobile_app_users",
    #     ),
    #     path(
    #         'total_nisponno/',
    #         views.total_nisponno,
    #         name="total_nisponno",
    #     ),
    #     path(
    #         'potrojari/',
    #         views.potrojari,
    #         name="potrojari",
    #     ),
    path(
        'total_upokarvogi',
        views.total_upokarvogi,
        name="total_upokarvogi",
    ),
    #     # path('analyze/', views.dashboard, name="analyze"),
    #     # path('analyze_disease/', views.analyze_disease, name="disease"),
    #     # path(
    #     #     'analyze_disease_monthwise/',
    #     #     views.analyze_disease_monthwise,
    #     #     name="analyze_disease_monthwise",
    #     # ),
    #     # path('compare_disease/', views.compare_diseases, name="compare_disease"),
    #     # path(
    #     #     'compare_diseases_monthwise/',
    #     #     views.compare_diseases_monthwise,
    #     #     name="compare_diseases_monthwise",
    #     # ),
    #     # path('analyze_age_group/', views.analyze_age_group, name="age_group_analysis"),
    #     # path('age_group_drilldown/', views.age_group_drilldown, name="age_group_drilldown"),
    #     # path(
    #     #     'analyze_consultation/', views.analyze_consultation, name="analyze_consultation"
    #     # ),
    #     # path(
    #     #     'analyze_consultation_detail/',
    #     #     views.analyze_consultation_detail,
    #     #     name="analyze_consultation_detail",
    #     # ),
    #     # # predict by month
    #     # path('predict_monthly_visit/', views.predict_monthly_visit, name='predict_monthly_visit'),
    #     # path('predict_monthly_visitor_count/', views.predict_monthly_visitor_count),
    #     # path('generate_view/', views.generate_view),
]
