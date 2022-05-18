from django.urls import path

from . import api, views

urlpatterns = [
    # path('', views.dashboard_home, name="dashboard_home"),
    path('', views.total_offices_view, name="dashboard_home"),
    path('total_offices/', views.total_offices_view, name="total_offices"),
    path(
        'nispottikritto_nothi/',
        views.nispottikritto_nothi_view,
        name="nispottikritto_nothi",
    ),
    path(
        'nothi_users_total/',
        views.nothi_users_total_view,
        name="nothi_users_total",
    ),
    path(
        'total_upokarvogi/',
        views.total_upokarvogi_view,
        name="total_upokarvogi",
    ),
    path(
        'nothi_users_male/',
        views.nothi_users_male_view,
        name="nothi_users_male",
    ),
    path(
        'nothi_users_female/',
        views.nothi_users_female_view,
        name="nothi_users_female",
    ),
    path(
        'note_nisponno/',
        views.note_nisponno_view,
        name="note_nisponno",
    ),
    path(
        'potrojari/',
        views.potrojari_view,
        name="potrojari",
    ),
    path(
        'custom_report/',
        views.custom_report,
        name="custom_report",
    ),
    path(
        'mobile_app_users/',
        views.mobile_app_users_view,
        name="mobile_app_users",
    ),
    path(
        'login_total_users/',
        views.login_total_users_view,
        name="login_total_users",
    ),
    path(
        'login_male_users/',
        views.login_male_users_view,
        name="login_male_users",
    ),
    path(
        'login_female_users/',
        views.login_female_users_view,
        name="login_female_users",
    ),
    path(
        'source_db_status/',
        api.SourceDBStatusAPI.as_view(),
        name="source_db_status",
    ),
    path(
        'report_db_status/',
        api.ReportDBStatus.as_view(),
        name="report_db_status",
    ),
    path(
        'dashboard_update_log/',
        api.DashboardUpdateLogAPI.as_view(),
        name="dashboard_update_log",
    ),
    path(
        'export_csv/<str:start_date>/<str:end_date>/',
        views.report_export_csv_view,
        name="export_csv",
    ),
]
