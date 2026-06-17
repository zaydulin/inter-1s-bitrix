from unittest.mock import Mock, patch

from django.test import Client, TestCase
from django.urls import reverse

from .models import SyncExecution
from .services import SyncResult, SyncService


class SyncServiceTests(TestCase):
    def test_run_both_aggregates_results(self):
        service = SyncService()
        service.sync_bitrix_to_onec = Mock(return_value=SyncResult(2, 2, "a"))
        service.sync_onec_to_bitrix = Mock(return_value=SyncResult(3, 3, "b"))

        execution = service.run(SyncExecution.DIRECTION_BOTH)

        self.assertEqual(execution.status, SyncExecution.STATUS_SUCCESS)
        self.assertEqual(execution.pulled_count, 5)
        self.assertEqual(execution.pushed_count, 5)


class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("sync_bridge.views.SyncService.run")
    def test_post_runs_manual_sync(self, run_mock):
        run_mock.return_value = SyncExecution(
            direction=SyncExecution.DIRECTION_BOTH,
            status=SyncExecution.STATUS_SUCCESS,
            pulled_count=4,
            pushed_count=4,
            message="ok",
        )

        response = self.client.post(
            reverse("sync_bridge:dashboard"),
            {"direction": SyncExecution.DIRECTION_BOTH},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        run_mock.assert_called_once_with(SyncExecution.DIRECTION_BOTH)
