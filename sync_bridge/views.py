from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from .forms import ManualSyncForm
from .models import SyncExecution
from .services import SyncService


class DashboardView(View):
    template_name = "sync_bridge/dashboard.html"

    def get(self, request):
        form = ManualSyncForm(initial={"direction": SyncExecution.DIRECTION_BOTH})
        executions = SyncExecution.objects.all()[:20]
        return render(request, self.template_name, {"form": form, "executions": executions})

    def post(self, request):
        form = ManualSyncForm(request.POST)
        if not form.is_valid():
            executions = SyncExecution.objects.all()[:20]
            return render(request, self.template_name, {"form": form, "executions": executions}, status=400)

        execution = SyncService().run(form.cleaned_data["direction"])
        if execution.status == SyncExecution.STATUS_SUCCESS:
            messages.success(request, f"Синхронизация завершена. Отправлено: {execution.pushed_count}.")
        else:
            messages.error(request, f"Синхронизация завершилась ошибкой: {execution.message}")
        return redirect("sync_bridge:dashboard")
