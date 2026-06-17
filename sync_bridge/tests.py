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

    def test_fetch_invoice_list_uses_post_json_list(self):
        service = SyncService()
        service.onec_client.post_json_list = Mock(return_value=[{"id": "1"}])

        result = service.fetch_invoice_list(date_from="2026-01-01", date_to="2026-01-31", inn="123")

        self.assertEqual(result, [{"id": "1"}])
        service.onec_client.post_json_list.assert_called_once_with(
            "/ut/hs/bitrixintegration/invoice/list",
            {"date_from": "2026-01-01", "date_to": "2026-01-31", "inn": "123"},
        )


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
        run_mock.assert_called_once_with(SyncExecution.DIRECTION_BOTH, date_from="", date_to="", inn="")

    @patch("sync_bridge.views.SyncService.fetch_invoice_list")
    def test_post_fetches_invoice_list(self, fetch_mock):
        fetch_mock.return_value = [{"number": "INV-1"}]

        response = self.client.post(
            reverse("sync_bridge:dashboard"),
            {
                "action": "fetch",
                "direction": SyncExecution.DIRECTION_ONEC_TO_BITRIX,
                "date_from": "2026-01-01",
                "date_to": "2026-01-31",
                "inn": "7701234567",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "INV-1")


class InvoiceListViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch("sync_bridge.views.SyncService.fetch_invoice_list")
    def test_post_fetches_invoice_list_by_date(self, fetch_mock):
        fetch_mock.return_value = [{"number": "INV-2026-01"}]

        response = self.client.post(
            reverse("sync_bridge:invoice_list"),
            {
                "date_from": "2026-01-01",
                "date_to": "2026-01-31",
                "inn": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        fetch_mock.assert_called_once_with(date_from="2026-01-01", date_to="2026-01-31", inn="")
        self.assertContains(response, "INV-2026-01")
