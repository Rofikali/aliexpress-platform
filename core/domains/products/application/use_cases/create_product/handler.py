# # file name: core/domains/products/application/use_cases/create_product/handler.py

# from core.domains.products.domain.aggregates.product_aggregate import ProductAggregate


# class CreateProductHandler:
#     def __init__(self, repository, event_publisher):
#         self.repository = repository
#         self.event_publisher = event_publisher

#     def handle(self, command):
#         aggregate = ProductAggregate.create(
#             product_id=command.product_id,
#             seller_id=command.seller_id,
#             title=command.title,
#         )

#         self.repository.save(aggregate)
#         self.event_publisher.publish_all(aggregate.pull_events())


import uuid
from core.domains.products.domain.aggregates.product_aggregate import ProductAggregate


class CreateProductHandler:
    def __init__(self, repository, event_publisher):
        self.repository = repository
        self.event_publisher = event_publisher

    def handle(self, command):
        product_id = uuid.uuid4()  # ✅ SYSTEM GENERATES ID

        aggregate = ProductAggregate.create(
            product_id=product_id,
            seller_id=command.seller_id,
            title=command.title,
        )

        self.repository.save(aggregate)
        self.event_publisher.publish_all(aggregate.pull_events())

        return aggregate  # optional but useful
