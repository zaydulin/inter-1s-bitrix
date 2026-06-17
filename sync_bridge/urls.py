from django.urls import path

from .views import DashboardView, InvoiceListView


app_name = "sync_bridge"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("invoice-list/", InvoiceListView.as_view(), name="invoice_list"),
]
