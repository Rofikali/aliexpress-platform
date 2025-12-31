from django.apps import AppConfig
from core.shared.observability.tracing.tracer import setup_tracing


class SharedConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.shared"

    def ready(self):
        setup_tracing()
        from core.shared.admin.outbox_admin import OutboxEventAdmin
