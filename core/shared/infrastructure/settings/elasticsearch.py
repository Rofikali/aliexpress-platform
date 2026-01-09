from django.conf import settings

ELASTICSEARCH_HOSTS = getattr(
    settings,
    "ELASTICSEARCH_HOSTS",
    ["http://elasticsearch:9200"],
)

ELASTICSEARCH_USER = getattr(
    settings,
    "ELASTICSEARCH_USER",
    None,
)

ELASTICSEARCH_PASSWORD = getattr(
    settings,
    "ELASTICSEARCH_PASSWORD",
    None,
)
