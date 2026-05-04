from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers

from store_app.models import Product, Category
from store_app.loguru_config import AppLogger

logger = AppLogger().get_logger()


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
        product = Product.objects.all()
        result = [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "price": c.price,
                "category": c.category.id,
            }
            for c in product
        ]
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
