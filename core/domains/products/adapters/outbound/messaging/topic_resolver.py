# core/domains/products/adapters/outbound/messaging/topic_resolver.py


def product_topic_resolver(outbox_event):
    """
    Maps outbox row → Kafka topic
    """
    return outbox_event.event_type
