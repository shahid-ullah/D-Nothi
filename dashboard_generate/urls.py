from django.urls import path

from . import views

urlpatterns = [
    path('', views.total_offices_view, name="total_offices"),
]
