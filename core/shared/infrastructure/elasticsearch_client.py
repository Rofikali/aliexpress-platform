from elasticsearch import Elasticsearch
from django.conf import settings

_es_client = None


def get_es_client():
    global _es_client
    if _es_client is None:
        _es_client = Elasticsearch(
            hosts=settings.ELASTICSEARCH_HOSTS,
            http_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD),
        )
    return _es_client
