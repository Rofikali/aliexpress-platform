# filename : core/shared/infrastructure/search/elasticsearch_client.py

from elasticsearch import Elasticsearch
from core.shared.infrastructure.settings.elasticsearch import (
    ELASTICSEARCH_HOSTS,
    ELASTICSEARCH_USER,
    ELASTICSEARCH_PASSWORD,
)

_es_client = None


def get_es_client():
    global _es_client
    if _es_client is None:
        kwargs = {"hosts": ELASTICSEARCH_HOSTS}

        if ELASTICSEARCH_USER and ELASTICSEARCH_PASSWORD:
            kwargs["http_auth"] = (
                ELASTICSEARCH_USER,
                ELASTICSEARCH_PASSWORD,
            )

        _es_client = Elasticsearch(**kwargs)

    return _es_client

