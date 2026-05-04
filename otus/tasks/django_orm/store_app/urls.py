from django.urls import path

from store_app.view import (
    AboutView,
    CategoryView,
    CategoryIdView,
    ProductView,
    ProductIdView,
    IndexView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("category/", CategoryView.as_view(), name="category"),
    path("category/<int:pk>/", CategoryIdView.as_view(), name="category_id"),
    path("product/", ProductView.as_view(), name="product"),
    path("product/<int:pk>/", ProductIdView.as_view(), name="product_id"),
]
