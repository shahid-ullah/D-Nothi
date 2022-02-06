from django.urls import path

from . import views

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
]
