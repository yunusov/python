from django.shortcuts import render
from rest_framework.views import APIView

from store_app.repository.product_repository import ProductRepository

pr = ProductRepository()


class AboutView(APIView):
    def get(self, request):
        """Страница о нас"""
        context = {
            "School": "OTUS",
            "Task": "Django ORM",
            "Year": "2026",
            "Student": "Vitaly Yunusov",
        }
        return render(
            request,
            "about.html",
            context,
        )


class IndexView(APIView):
    def get(self, request):
        """Страница index"""
        products = pr.get_all_products()
        context = {
            "products": products,
        }
        return render(request, "index.html", context)
