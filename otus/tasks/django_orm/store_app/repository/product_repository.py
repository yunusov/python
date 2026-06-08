from store_app.loguru_config import AppLogger
from store_app.models import Product

logger = AppLogger().get_logger()


class ProductRepository():
    def get_all_products(self) -> list:
        products = Product.objects.select_related('category').all()
        result = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": product.category.name,
            }
            for product in products
        ]
        return result
    
    def get_product(self, product_id) -> dict:
        product = Product.objects.select_related('category').filter(id=product_id).first()
        if product:
            return  {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "category": product.category.name,
                    "created_at": product.created_at,
                }
        return {}