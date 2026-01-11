# # # # filename : core/domains/products/management/commands/rebuild_product_search_projection.py

# # import logging
# # from django.core.management.base import BaseCommand
# # import uuid

# # from core.domains.products.read_model.indices.product_search_index import (
# #     PRODUCT_SEARCH_MAPPING,
# # )
# # from core.domains.products.read_model.rebuild.rebuild_product_read_model import (
# #     replay_product_events,
# # )

# # from core.shared.infrastructure.search.elasticsearch_client import get_es_client


# # class Command(BaseCommand):
# #     logging.debug(
# #         "Rebuild Product Search Projection Command : "
# #         "core/domains/products/management/commands/rebuild_product_search_projection.py"
# #     )
# #     help = "Rebuild product search projection from Kafka"

# #     def handle(self, *args, **options):
# #         es = get_es_client()
# #         version = uuid.uuid4().hex[:6]
# #         index_name = f"product_search_v1_{version}"

# #         self.stdout.write(f"Creating index {index_name}")
# #         es.indices.create(index=index_name, body=PRODUCT_SEARCH_MAPPING)

# #         self.stdout.write("Replaying Kafka events...")
# #         count = replay_product_events(index_name)

# #         self.stdout.write(f"Replayed {count} events")

# #         self.stdout.write("Switching alias")
# #         es.indices.update_aliases(
# #             body={
# #                 "actions": [
# #                     {"remove": {"alias": "product_search_current", "index": "*"}},
# #                     {"add": {"alias": "product_search_current", "index": index_name}},
# #                 ]
# #             }
# #         )

# #         self.stdout.write(self.style.SUCCESS("Projection rebuild complete"))


# import logging
# from django.core.management.base import BaseCommand
# import uuid

# from core.domains.products.read_model.indices.product_search_index import (
#     PRODUCT_SEARCH_MAPPING,
# )
# from core.domains.products.read_model.rebuild.rebuild_product_read_model import (
#     replay_product_events,
# )
# from core.shared.infrastructure.search.elasticsearch_client import get_es_client


# class Command(BaseCommand):
#     logging.debug(
#         "Rebuild Product Search Projection Command : "
#         "core/domains/products/management/commands/rebuild_product_search_projection.py"
#     )
#     help = "Rebuild product search projection from Kafka"

#     def handle(self, *args, **options):
#         es = get_es_client()
#         version = uuid.uuid4().hex[:6]
#         index_name = f"product_search_v1_{version}"

#         self.stdout.write(f"Creating index {index_name}")
#         es.indices.create(index=index_name, body=PRODUCT_SEARCH_MAPPING)

#         self.stdout.write("Replaying Kafka events...")
#         count = replay_product_events(index_name)

#         self.stdout.write(f"Replayed {count} events")

#         self.stdout.write("Switching alias")
#         es.indices.update_aliases(
#             body={
#                 "actions": [
#                     {"remove": {"alias": "product_search_current", "index": "*"}},
#                     {"add": {"alias": "product_search_current", "index": index_name}},
#                 ]
#             }
#         )

#         self.stdout.write(self.style.SUCCESS("Projection rebuild complete"))


from django.core.management.base import BaseCommand
from core.domains.products.read_model.repositories.product_search_repository import (
    ProductSearchRepository,
)
from core.domains.products.read_model.documents.product_search_document import (
    ProductSearchDocument,
)

from core.domains.products.adapters.outbound.persistence.models.product_model import (
    ProductModel,
)

from core.shared.infrastructure.search.elasticsearch_client import get_es_client


class Command(BaseCommand):
    help = "Rebuild product search projection from database"

    def handle(self, *args, **options):
        es = get_es_client()
        repo = ProductSearchRepository()

        self.stdout.write("Rebuilding product search projection...")

        for product in ProductModel.objects.iterator():
            document = ProductSearchDocument(
                id=str(product.id),
                title=product.title,
                seller_id=str(product.seller_id),
                price=product.price,
                status=product.status,
                occurred_at=product.created_at,
            )

            es.index(
                index=repo.INDEX_ALIAS,
                id=document.id,
                document=document.to_dict(),
            )

        self.stdout.write(self.style.SUCCESS("Projection rebuild complete"))
