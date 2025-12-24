from django.db import models


class DeadLetterEvent(models.Model):
    id = models.UUIDField(primary_key=True)
    topic = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255)
    payload = models.JSONField()
    retry_count = models.IntegerField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        default="PENDING",  # PENDING | REPLAYED | FAILED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    replayed_at = models.DateTimeField(null=True, blank=True)
