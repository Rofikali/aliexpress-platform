from django.contrib import admin
from core.shared.read_model.models.dlq_event import DeadLetterEvent


@admin.register(DeadLetterEvent)
class DeadLetterEventAdmin(admin.ModelAdmin):
    list_display = ("id", "event_type", "status", "created_at")
    actions = ["replay_selected"]

    def replay_selected(self, request, queryset):
        from core.shared.application.dlq_replay_service import DLQReplayService

        service = DLQReplayService()
        for event in queryset:
            service.replay(event.id)
