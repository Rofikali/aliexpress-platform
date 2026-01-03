def generate_dlq_topic(original_topic: str, prefix: str = "dlq.") -> str:
    return f"{prefix}{original_topic}"
