# config/urls.py

from automate_process.api import (
    BackupDBLogAPI,
    DatabaseBackupLog,
    ReportGenerationLogAPI,
    SourceDBLogAPI,
    updateDashboard,
)
from backup_source_db.models import BackupDBLog
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from users.views import logout_view, sso_login_handler

urlpatterns = [
    path('', include('dashboard_generate.urls')),
    # path('monthly_report/', include('monthly_report.urls')),
    path('update_dashboard/', updateDashboard.as_view()),
    path('backup_log/', DatabaseBackupLog.as_view()),
    path('source_db_log/', SourceDBLogAPI.as_view(), name='source_db_log'),
    path('backup_db_log/', BackupDBLogAPI.as_view(), name='backup_db_log'),
    path('report_generation_log/', ReportGenerationLogAPI.as_view(), name='report_generation_log'),
    path('((thele$$!!/', admin.site.urls),
    path('sso_login_handler/', sso_login_handler, name='sso_login_handler'),
    path('logout/', logout_view, name='logout'),
    # path('api-auth/', include('rest_framework.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += (path('__debug__/', include('debug_toolbar.urls')),)

admin.site.site_header = "D-Nothi admin"
admin.site.site_title = "D-Nothi admin"
admin.site.index_title = "Welcome to D-Nothi Dashboard"
