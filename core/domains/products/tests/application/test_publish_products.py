from unittest.mock import Mock
from core.domains.products.application.use_cases.publish_product.handler import (
    PublishProductHandler,
)
form core.domains.products.tests.domain.test_fixtures import fake_product


def test_publish_product_success():
    repo = Mock()
    publisher = Mock()

    repo.get.return_value = fake_product()

    handler = PublishProductHandler(repo, publisher)
    handler.execute(product_id="prod-1")

    publisher.publish.assert_called()
