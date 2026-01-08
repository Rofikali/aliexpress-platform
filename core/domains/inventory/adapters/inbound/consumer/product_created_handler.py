# from core.domains.inventory.application.use_cases.create_inventory_for_product.command import CreateInventoryForProductCommand

from core.domains.inventory.application.use_cases.create_inventory_for_product.handler import (
    CreateInventoryForProductHandler,
)
from core.domains.inventory.application.use_cases.create_inventory_for_product.command import (
    CreateInventoryForProductCommand,
)
from core.domains.inventory.adapters.outbound.persistence.inventory_repository_impl import (
    InventoryRepositoryImpl,
)

import logging
class ProductCreatedHandler:

    def handle(self, event):
        logging.debug(
            f"Handling product.created DLQ event for aggregate_id {event['aggregate_id']} "
            f"and filename : core/domains/inventory/adapters/inbound/consumer/product_created_handler.py"
        )
        command = CreateInventoryForProductCommand(product_id=event["aggregate_id"])

        handler = CreateInventoryForProductHandler(repository=InventoryRepositoryImpl())

        handler.handle(command)
