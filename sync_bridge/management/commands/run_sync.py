from django.core.management.base import BaseCommand, CommandError

from sync_bridge.models import SyncExecution
from sync_bridge.services import SyncService


class Command(BaseCommand):
    help = "Запускает ручную синхронизацию между Bitrix и 1C."

    def add_arguments(self, parser):
        parser.add_argument(
            "--direction",
            default=SyncExecution.DIRECTION_BOTH,
            choices=[
                SyncExecution.DIRECTION_BITRIX_TO_ONEC,
                SyncExecution.DIRECTION_ONEC_TO_BITRIX,
                SyncExecution.DIRECTION_BOTH,
            ],
            help="Направление синхронизации.",
        )
        parser.add_argument("--date-from", default="", help="Фильтр даты начала в формате YYYY-MM-DD.")
        parser.add_argument("--date-to", default="", help="Фильтр даты окончания в формате YYYY-MM-DD.")
        parser.add_argument("--inn", default="", help="Фильтр по ИНН.")

    def handle(self, *args, **options):
        execution = SyncService().run(
            options["direction"],
            date_from=options["date_from"],
            date_to=options["date_to"],
            inn=options["inn"],
        )
        if execution.status == SyncExecution.STATUS_FAILED:
            raise CommandError(execution.message)
        self.stdout.write(
            self.style.SUCCESS(
                f"Готово. pulled={execution.pulled_count}, pushed={execution.pushed_count}"
            )
        )
