import logging
import json


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }

        if hasattr(record, "extra"):
            log_record.update(record.extra)

        return json.dumps(log_record)


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    logger.handlers.clear()
    logger.addHandler(handler)

    return logger
