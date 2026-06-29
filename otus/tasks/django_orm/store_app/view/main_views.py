from django.shortcuts import render
from rest_framework.views import APIView
from django.views.generic import ListView

from store_app.models import Product
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


class IndexView(ListView):
    model = Product
    template_name = "index.html"
    context_object_name = 'products'
