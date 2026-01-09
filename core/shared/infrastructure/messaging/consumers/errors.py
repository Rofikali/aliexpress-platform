# class RetryableError(Exception):
#     """Temporary failure (DB down, timeout, network)"""

#     pass


# class NonRetryableError(Exception):
#     """Permanent failure (business rule, invalid state)"""

#     pass

# # filename : core/shared/infrastructure/messaging/consumers/errors.py
# Staff-grade error taxonomy


class ConsumerError(Exception):
    """Base class for all consumer errors"""


class BusinessError(ConsumerError):
    """Non-retryable business failure (goes to DLQ)"""


class RetryableBusinessError(BusinessError):
    """Retryable business failure (goes to retry topic)"""


class InfrastructureError(ConsumerError):
    """Infra/config/system failure (crash consumer)"""
