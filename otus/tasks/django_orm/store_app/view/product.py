from django.shortcuts import get_object_or_404, render, redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers

from store_app.loguru_config import AppLogger
from store_app.models import Product, Category
from store_app.forms import ProductEditForm, ProductForm
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
        result = pr.get_all_products
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


class ProductDetailView(APIView):
    def get(self, request, product_id):
        """Показать продукт"""
        logger.info(f"Показать продукт {product_id}")
        product = pr.get_product(product_id)
        context = {
            "product": product,
        }
        return render(request, "product_detail.html", context)


class ProductEditView(APIView):
    def get(self, request, product_id):
        product = (
            Product.objects.select_related("category").filter(id=product_id).first()
        )
        form = ProductEditForm(instance=product)
        context = {"form": form, "title": "Редактирование продукта"}
        return render(request, "product_edit.html", context=context)

    def post(self, request, product_id):
        """Редактировать продукт"""
        logger.info(f"Редактировать продукт {product_id}")
        product = (
            Product.objects.select_related("category").filter(id=product_id).first()
        )
        form = ProductEditForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("index")
        context = {
            "form": form,
            "title": "Редактировать пост",
        }
        return render(request, "product_edit.html", context=context)


class ProductAddView(APIView):
    def get(self, request):
        form = ProductForm()
        context = {"form": form}
        return render(request, "product_add.html", context=context)

    def post(self, request):
        """Добавить продукт"""
        form = ProductForm(request.POST)
        if form.is_valid():
            Product.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                price=form.cleaned_data["price"],
                category=form.cleaned_data["category"],
            )
            return redirect("index")


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
