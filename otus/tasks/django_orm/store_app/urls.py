from django.urls import path

from store_app.view import (
    AboutView,
    CategoryView,
    CategoryAddView,
    CategoryIdView,
    ProductAddView,
    ProductDetailView,
    ProductEditView,
    ProductDeleteView,
    ProductView,
    ProductIdView,
    IndexView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("category/", CategoryView.as_view(), name="category"),
    path("category/create/", CategoryAddView.as_view(), name="category_add"),
    path("category/<int:pk>/", CategoryIdView.as_view(), name="category_id"),
    path("product/", ProductView.as_view(), name="product"),
    path("product/create/", ProductAddView.as_view(), name="product_add"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/<int:pk>/edit/", ProductEditView.as_view(), name="product_edit"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("api/product/<int:pk>/", ProductIdView.as_view(), name="product_id"),
]
