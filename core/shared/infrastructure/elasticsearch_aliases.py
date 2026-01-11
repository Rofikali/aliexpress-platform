import logging

from elasticsearch import Elasticsearch

logging.basicConfig(level=logging.INFO)
logging.debug(
    "this file calling filename : core/shared/infrastructure/elasticsearch_aliases.py",
    __name__,
)


def switch_alias(es, alias: str, new_index: str):
    actions = []

    if es.indices.exists_alias(name=alias):
        old_indices = list(es.indices.get_alias(name=alias).keys())
        for old in old_indices:
            actions.append({"remove": {"index": old, "alias": alias}})

    actions.append({"add": {"index": new_index, "alias": alias}})

    es.indices.update_aliases({"actions": actions})
