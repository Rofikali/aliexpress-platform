MAX_RETRIES = 3


def should_retry(event: dict) -> bool:
    return event.get("retry_count", 0) < MAX_RETRIES


def increment_retry(event: dict) -> dict:
    event["retry_count"] = event.get("retry_count", 0) + 1
    return event
