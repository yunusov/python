from django.shortcuts import get_object_or_404, render, redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from rest_framework import status, serializers
from django.urls import reverse_lazy
from django.contrib import messages

from store_app.loguru_config import AppLogger
from store_app.models import Product, Category
from store_app.forms import ProductEditForm
from store_app.repository.product_repository import ProductRepository

logger = AppLogger().get_logger()
pr = ProductRepository()


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, help_text="Название продукта")
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Описание категории",
    )
    price = serializers.FloatField(
        required=False,
        help_text="Цена",
    )
    category = serializers.IntegerField(
        help_text="ID категории",
    )


class ProductView(APIView):
    def get(self, request):
        """Показать все продукты"""
        result = pr.get_all_products()
        return Response(result)

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        """Добавить продукт"""
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = request.data.get("name")
        description = request.data.get("description")
        price = request.data.get("price")
        category_id = request.data.get("category")
        category = get_object_or_404(Category, id=category_id)

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
        )
        return Response(
            {
                "status": "ok",
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": product.category.id,
            },
            status=status.HTTP_201_CREATED,
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class ProductEditView(UpdateView):
    """Редактирование поста."""
    model = Product
    template_name = 'product_edit.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('index')


    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно изменён')
        return super().form_valid(form)


class ProductAddView(CreateView):
    """Добавление нового поста."""
    model = Product
    template_name = 'product_add.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('index')


    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно создан')
        return super().form_valid(form)


class ProductIdView(APIView):

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, pk):
        """Изменить продукт"""
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = request.data.get("name")
        description = request.data.get("description")
        price = request.data.get("price")
        category_id = request.data.get("category")
        category = get_object_or_404(Category, pk=category_id)

        product = get_object_or_404(Product, pk=pk)
        product.name = name
        product.description = description
        product.price = price
        product.category = category
        product.save()

        return Response(
            {
                "status": "ok",
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": product.category.id,
            },
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, pk):
        """Удалить продукт"""
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({})
    

class ProductDeleteView(DeleteView):
    """Удаление продукта."""
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        context['title'] = "Удалить продукт"
        return context
    