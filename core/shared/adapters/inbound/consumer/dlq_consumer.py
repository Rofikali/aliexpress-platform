# def handle_dlq_event(event):
#     # save to postgres
#     # alert via Slack / email
#     # allow replay later
#     pass


from core.shared.read_model.models.dlq_event import DeadLetterEvent


def handle_dlq_event(event):
    DeadLetterEvent.objects.create(
        id=event["aggregate_id"],
        topic=event.get("topic"),
        event_type=event["type"],
        payload=event["payload"],
        retry_count=event["retry_count"],
        reason=event["dlq_reason"],
    )
