# config/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from automate_process.api import updateDashboard, DatabaseBackupLog
from users.views import logout_view, sso_login_handler

urlpatterns = [
    path('', include('dashboard_generate.urls')),
    # path('monthly_report/', include('monthly_report.urls')),
    path('update_dashboard/', updateDashboard.as_view()),
    path('backup_log/', DatabaseBackupLog.as_view()),
    path('((thele$$!!/', admin.site.urls),
    path('sso_login_handler/', sso_login_handler, name='sso_login_handler'),
    path('logout/', logout_view, name='logout'),
    # path('api-auth/', include('rest_framework.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += (path('__debug__/', include('debug_toolbar.urls')), )

admin.site.site_header = "D-Nothi admin"
admin.site.site_title = "D-Nothi admin"
admin.site.index_title = "Welcome to D-Nothi Dashboard"
