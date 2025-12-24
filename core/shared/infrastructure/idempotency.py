from django.core.cache import cache


def already_processed(event_id: str) -> bool:
    return cache.get(event_id) is True


def mark_processed(event_id: str):
    cache.set(event_id, True, timeout=86400)
