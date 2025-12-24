import logging

audit_logger = logging.getLogger("audit")


def log_action(action, actor_id, target_id):
    audit_logger.info(
        {"action": action, "actor": str(actor_id), "target": str(target_id)}
    )
