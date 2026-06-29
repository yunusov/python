from .category import CategoryView, CategoryIdView, CategoryAddView
from .product import (
    ProductView,
    ProductIdView,
    ProductAddView,
    ProductDetailView,
    ProductEditView,
    ProductDeleteView,
)
from .main_views import IndexView, AboutView

__all__ = [
    "CategoryView",
    "CategoryAddView",
    "CategoryIdView",
    "ProductView",
    "IndexView",
    "ProductAddView",
    "ProductDetailView",
    "ProductIdView",
    "AboutView",
    "ProductEditView",
    "ProductDeleteView",
]
