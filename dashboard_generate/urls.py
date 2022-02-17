from django.urls import path

from . import api, views

urlpatterns = [
    path('', views.total_offices_view, name="total_offices"),
    path('', views.total_offices_view, name="home"),
    path(
        'nispottikritto_nothi/',
        views.nispottikritto_nothi_view,
        name="nispottikritto_nothi",
    ),
    path(
        'nothi_users_total/',
        views.nothi_users_total,
        name="nothi_users_total",
    ),
    path(
        'total_upokarvogi/',
        views.total_upokarvogi,
        name="total_upokarvogi",
    ),
    path(
        'nothi_users_male/',
        views.nothi_users_male,
        name="nothi_users_male",
    ),
    path(
        'nothi_users_female/',
        views.nothi_users_female,
        name="nothi_users_female",
    ),
    path(
        'note_nisponno/',
        views.note_nisponno,
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
        'export_csv/<str:start_date>/<str:end_date>/',
        views.report_export_csv,
        name="export_csv",
    ),
]
