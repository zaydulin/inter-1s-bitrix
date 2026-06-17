from dataclasses import dataclass

from django.conf import settings
from django.utils import timezone

from .clients import HttpClient, IntegrationError, build_basic_auth
from .models import SyncExecution


@dataclass
class SyncResult:
    pulled_count: int = 0
    pushed_count: int = 0
    message: str = ""


class SyncService:
    def __init__(self) -> None:
        bitrix_headers = {}
        if settings.BITRIX_AUTH_TOKEN:
            bitrix_headers["Authorization"] = f"Bearer {settings.BITRIX_AUTH_TOKEN}"

        onec_headers = {}
        if settings.ONEC_USERNAME or settings.ONEC_PASSWORD:
            onec_headers["Authorization"] = build_basic_auth(
                settings.ONEC_USERNAME,
                settings.ONEC_PASSWORD,
            )

        self.bitrix_client = HttpClient(
            base_url=settings.BITRIX_BASE_URL,
            timeout=settings.BITRIX_TIMEOUT,
            headers=bitrix_headers,
        )
        self.onec_client = HttpClient(
            base_url=settings.ONEC_BASE_URL,
            timeout=settings.ONEC_TIMEOUT,
            headers=onec_headers,
        )

    def run(self, direction: str) -> SyncExecution:
        execution = SyncExecution.objects.create(direction=direction)
        try:
            if direction == SyncExecution.DIRECTION_BITRIX_TO_ONEC:
                result = self.sync_bitrix_to_onec()
            elif direction == SyncExecution.DIRECTION_ONEC_TO_BITRIX:
                result = self.sync_onec_to_bitrix()
            elif direction == SyncExecution.DIRECTION_BOTH:
                first = self.sync_bitrix_to_onec()
                second = self.sync_onec_to_bitrix()
                result = SyncResult(
                    pulled_count=first.pulled_count + second.pulled_count,
                    pushed_count=first.pushed_count + second.pushed_count,
                    message="Bitrix -> 1C; 1C -> Bitrix",
                )
            else:
                raise IntegrationError(f"Неизвестное направление синхронизации: {direction}")

            execution.status = SyncExecution.STATUS_SUCCESS
            execution.pulled_count = result.pulled_count
            execution.pushed_count = result.pushed_count
            execution.message = result.message
        except Exception as exc:
            execution.status = SyncExecution.STATUS_FAILED
            execution.message = str(exc)
        finally:
            execution.finished_at = timezone.now()
            execution.save()

        return execution

    def sync_bitrix_to_onec(self) -> SyncResult:
        items = self.bitrix_client.get_json(settings.BITRIX_SOURCE_PATH)
        pushed = 0
        for item in items:
            self.onec_client.post_json(settings.ONEC_TARGET_PATH, item)
            pushed += 1
        return SyncResult(
            pulled_count=len(items),
            pushed_count=pushed,
            message="Данные выгружены из Bitrix и отправлены в 1C.",
        )

    def sync_onec_to_bitrix(self) -> SyncResult:
        items = self.onec_client.get_json(settings.ONEC_SOURCE_PATH)
        pushed = 0
        for item in items:
            self.bitrix_client.post_json(settings.BITRIX_TARGET_PATH, item)
            pushed += 1
        return SyncResult(
            pulled_count=len(items),
            pushed_count=pushed,
            message="Данные выгружены из 1C и отправлены в Bitrix.",
        )
