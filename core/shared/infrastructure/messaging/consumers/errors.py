# filename : core/shared/infrastructure/messaging/consumers/errors.py
class RetryableError(Exception):
    """Temporary failure (DB down, timeout, network)"""

    pass


class NonRetryableError(Exception):
    """Permanent failure (business rule, invalid state)"""

    pass
