# MAX_RETRIES = 3


# def should_retry(event: dict) -> bool:
#     return event.get("retry_count", 0) < MAX_RETRIES


# def increment_retry(event: dict) -> dict:
#     event["retry_count"] = event.get("retry_count", 0) + 1
#     return event


# filename : core/shared/infrastructure/messaging/consumers/retry_policy.py
from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 5
    base_delay_seconds: int = 2
    backoff_multiplier: int = 2

    def delay_for_attempt(self, attempt: int) -> int:
        return self.base_delay_seconds * (self.backoff_multiplier ** (attempt - 1))
