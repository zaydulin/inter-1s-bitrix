from django.contrib import admin

from .models import SyncExecution


@admin.register(SyncExecution)
class SyncExecutionAdmin(admin.ModelAdmin):
    list_display = ("id", "direction", "status", "pulled_count", "pushed_count", "started_at", "finished_at")
    list_filter = ("direction", "status", "started_at")
    search_fields = ("message",)
