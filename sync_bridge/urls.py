from django.urls import path

from .views import DashboardView


app_name = "sync_bridge"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
]
