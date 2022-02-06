from django.urls import path

from . import views

urlpatterns = [
    path('', views.total_offices_view, name="total_offices"),
    path('', views.total_offices_view, name="home"),
    path(
        'nispottikritto_nothi',
        views.nispottikritto_nothi_view,
        name="nispottikritto_nothi",
    ),
]
