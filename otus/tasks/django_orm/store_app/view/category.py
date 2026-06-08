from django.shortcuts import get_object_or_404, redirect, render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers

from store_app.forms import CategoryForm
from store_app.models import Category


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, help_text="Название категории")
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Описание категории",
    )


class CategoryView(APIView):
    def get(self, request):
        """Показать все категории"""
        category = Category.objects.all()
        result = [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
            }
            for c in category
        ]
        return Response(result)

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        """Добавление категории"""
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = request.data.get("name")
        description = request.data.get("description")

        category = Category.objects.create(
            name=name,
            description=description,
        )
        return Response(
            {
                "status": "ok",
                "id": category.id,
                "name": category.name,
            },
            status=status.HTTP_201_CREATED,
        )
    
class CategoryAddView(APIView):
    def get(self, request):
        form = CategoryForm()
        context = {"form": form}
        return render(request, "category_add.html", context=context)

    def post(self, request):
        """Добавить продукт"""
        form = CategoryForm(request.POST)
        if form.is_valid():
            Category.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
            )
            return redirect("index")


class CategoryIdView(APIView):

    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, pk):
        """Изменить категорию"""
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = request.data.get("name")
        description = request.data.get("description")

        сategory = get_object_or_404(Category, pk=pk)
        сategory.name = name
        сategory.description = description
        сategory.save()

        return Response(
            {
                "status": "ok",
                "id": сategory.id,
                "name": сategory.name,
                "description": сategory.description,
            },
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, pk):
        """Удалить категорию"""
        product = get_object_or_404(Category, pk=pk)
        product.delete()
        return Response({})
