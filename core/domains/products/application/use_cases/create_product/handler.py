from core.domains.products.domain.aggregates.product_aggregate import ProductAggregate


class CreateProductHandler:
    def __init__(self, repository, event_publisher):
        self.repository = repository
        self.event_publisher = event_publisher

    def handle(self, command):
        aggregate = ProductAggregate.create(
            product_id=command.product_id,
            seller_id=command.seller_id,
            title=command.title,
        )

        self.repository.save(aggregate)
        self.event_publisher.publish_all(aggregate.pull_events())
