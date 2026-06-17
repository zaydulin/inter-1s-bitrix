from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from .forms import InvoiceListForm, ManualSyncForm
from .models import SyncExecution
from .services import SyncService


class DashboardView(View):
    template_name = "sync_bridge/dashboard.html"

    def get(self, request):
        form = ManualSyncForm(initial={"direction": SyncExecution.DIRECTION_BOTH, "action": "fetch"})
        executions = SyncExecution.objects.all()[:20]
        return render(request, self.template_name, {"form": form, "executions": executions, "invoice_list": [], "invoice_count": 0})

    def post(self, request):
        form = ManualSyncForm(request.POST)
        executions = SyncExecution.objects.all()[:20]
        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "executions": executions, "invoice_list": [], "invoice_count": 0}, status=400)

        service = SyncService()
        filters = {
            "date_from": form.cleaned_data["date_from"].isoformat() if form.cleaned_data["date_from"] else "",
            "date_to": form.cleaned_data["date_to"].isoformat() if form.cleaned_data["date_to"] else "",
            "inn": form.cleaned_data["inn"],
        }
        if form.cleaned_data["action"] == "fetch":
            try:
                invoice_list = service.fetch_invoice_list(**filters)
            except Exception as exc:
                messages.error(request, f"Не удалось получить список: {exc}")
                return render(request, self.template_name, {"form": form, "executions": executions, "invoice_list": [], "invoice_count": 0}, status=502)

            messages.success(request, f"Получено счетов: {len(invoice_list)}.")
            return render(
                request,
                self.template_name,
                {"form": form, "executions": executions, "invoice_list": invoice_list, "invoice_count": len(invoice_list)},
            )

        execution = service.run(form.cleaned_data["direction"], **filters)
        if execution.status == SyncExecution.STATUS_SUCCESS:
            messages.success(request, f"Синхронизация завершена. Отправлено: {execution.pushed_count}.")
        else:
            messages.error(request, f"Синхронизация завершилась ошибкой: {execution.message}")
        return redirect("sync_bridge:dashboard")


class InvoiceListView(View):
    template_name = "sync_bridge/invoice_list.html"

    def get(self, request):
        form = InvoiceListForm()
        return render(request, self.template_name, {"form": form, "invoice_list": [], "invoice_count": 0})

    def post(self, request):
        form = InvoiceListForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"form": form, "invoice_list": [], "invoice_count": 0},
                status=400,
            )

        filters = {
            "date_from": form.cleaned_data["date_from"].isoformat() if form.cleaned_data["date_from"] else "",
            "date_to": form.cleaned_data["date_to"].isoformat() if form.cleaned_data["date_to"] else "",
            "inn": form.cleaned_data["inn"],
        }
        try:
            invoice_list = SyncService().fetch_invoice_list(**filters)
        except Exception as exc:
            messages.error(request, f"Не удалось получить список: {exc}")
            return render(
                request,
                self.template_name,
                {"form": form, "invoice_list": [], "invoice_count": 0},
                status=502,
            )

        messages.success(request, f"Получено счетов: {len(invoice_list)}.")
        return render(
            request,
            self.template_name,
            {"form": form, "invoice_list": invoice_list, "invoice_count": len(invoice_list)},
        )
