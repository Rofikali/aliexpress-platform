from django.core.management.base import BaseCommand
from core.shared.application.dlq_replay_service import DLQReplayService


class Command(BaseCommand):
    help = "Replay a DLQ event safely"

    def add_arguments(self, parser):
        parser.add_argument("event_id")

    def handle(self, *args, **options):
        service = DLQReplayService()
        service.replay(options["event_id"])
        self.stdout.write("DLQ event replayed")
