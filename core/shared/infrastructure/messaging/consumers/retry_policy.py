# # # filename : core/shared/infrastructure/messaging/consumers/retry_policy.py
# from dataclasses import dataclass
# from typing import Dict

# # have to share this codebase

# DEFAULT_MAX_RETRIES = 5


# def _get_meta(event: Dict) -> Dict:
#     return event.setdefault("meta", {})


# def should_retry(event: Dict) -> bool:
#     meta = _get_meta(event)

#     retry_count = meta.get("retry_count", 0)
#     max_retries = meta.get("max_retries", DEFAULT_MAX_RETRIES)

#     return retry_count < max_retries


# def increment_retry(event: Dict) -> Dict:
#     meta = _get_meta(event)

#     meta["retry_count"] = meta.get("retry_count", 0) + 1
#     meta.setdefault("max_retries", DEFAULT_MAX_RETRIES)

#     return event


# @dataclass(frozen=True)
# class RetryPolicy:
#     max_attempts: int = DEFAULT_MAX_RETRIES
#     base_delay_seconds: int = 2
#     backoff_multiplier: int = 2

#     def delay_for_attempt(self, attempt: int) -> int:
#         return self.base_delay_seconds * (self.backoff_multiplier ** (attempt - 1))

# filename : core/shared/infrastructure/messaging/consumers/retry_policy.py
MAX_RETRIES = 3


def should_retry(envelope: dict) -> bool:
    return envelope.get("retries", 0) < MAX_RETRIES
