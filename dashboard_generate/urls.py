from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from . import apis, views

CACHE_TTL = getattr(settings, 'CACHE_TTL', 10)
if settings.DEBUG:
    urlpatterns = [
        path('', views.dashboard_home, name="dashboard_home"),
        path('total_offices/', views.total_offices_view, name="total_offices"),
        path('ministry_wise_total_login/', views.ministry_wise_total_login_view, name="ministry_wise_total_login"),
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
            'dashboard_update_log/',
            apis.DashboardUpdateLogAPI.as_view(),
            name="dashboard_update_log",
        ),
        path(
            'export_csv/<str:start_date>/<str:end_date>/',
            views.report_export_csv_view,
            name="export_csv",
        ),
        path('v1/login_users_not_distinct/', apis.LoginUsersNotDistinctAPI.as_view(), name='login_users_not_distinct'),
        path('v1/clear_cache/', apis.ClearCacheAPI.as_view(), name='clear_cache'),
        path('report_summary/', views.report_summary, name='report_summary'),
        path('enothi_report/', views.office_wise_report_summary, name='office_wise_report_summary'),
    ]


else:
    urlpatterns = [
        path('', cache_page(CACHE_TTL, key_prefix='dashboard')(views.dashboard_home), name="dashboard_home"),
        path(
            'total_offices/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.total_offices_view),
            name="total_offices",
        ),
        path(
            'ministry_wise_total_login/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.ministry_wise_total_login_view),
            name="ministry_wise_total_login",
        ),
        path(
            'nispottikritto_nothi/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.nispottikritto_nothi_view),
            name="nispottikritto_nothi",
        ),
        path(
            'nothi_users_total/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.nothi_users_total_view),
            name="nothi_users_total",
        ),
        path(
            'total_upokarvogi/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.total_upokarvogi_view),
            name="total_upokarvogi",
        ),
        path(
            'nothi_users_male/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.nothi_users_male_view),
            name="nothi_users_male",
        ),
        path(
            'nothi_users_female/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.nothi_users_female_view),
            name="nothi_users_female",
        ),
        path(
            'note_nisponno/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.note_nisponno_view),
            name="note_nisponno",
        ),
        path(
            'potrojari/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.potrojari_view),
            name="potrojari",
        ),
        path(
            'custom_report/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.custom_report),
            name="custom_report",
        ),
        path(
            'mobile_app_users/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.mobile_app_users_view),
            name="mobile_app_users",
        ),
        path(
            'login_total_users/',
            cache_page(CACHE_TTL)(views.login_total_users_view),
            name="login_total_users",
        ),
        path(
            'login_male_users/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.login_male_users_view),
            name="login_male_users",
        ),
        path(
            'login_female_users/',
            cache_page(CACHE_TTL, key_prefix='dashboard')(views.login_female_users_view),
            name="login_female_users",
        ),
        path(
            'dashboard_update_log/',
            apis.DashboardUpdateLogAPI.as_view(),
            name="dashboard_update_log",
        ),
        path(
            'export_csv/<str:start_date>/<str:end_date>/',
            views.report_export_csv_view,
            name="export_csv",
        ),
        path('v1/login_users_not_distinct/', apis.LoginUsersNotDistinctAPI.as_view(), name='login_users_not_distinct'),
        path('v1/clear_cache/', apis.ClearCacheAPI.as_view(), name='clear_cache'),
        path('report_summary/', views.report_summary, name='report_summary'),
        path('enothi_report/', views.office_wise_report_summary, name='office_wise_report_summary'),
    ]
