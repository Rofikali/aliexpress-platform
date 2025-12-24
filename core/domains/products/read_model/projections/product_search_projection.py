from core.shared.infrastructure.elasticsearch_client import get_es_client


class ProductSearchProjection:
    INDEX = "product_search"

    def index(self, product):
        es = get_es_client()
        es.index(index=self.INDEX, id=str(product["id"]), document=product)

    def delete(self, product_id):
        es = get_es_client()
        es.delete(index=self.INDEX, id=str(product_id), ignore=[404])
