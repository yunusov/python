import pytest
from store_app.models import Category, Product


@pytest.mark.django_db
def test_create_products(product_1, product_2, product_3):
    """Проверка создания объекта автора."""
    assert Product.objects.count() == 3
    assert product_1.name == "product_1"
    assert product_2.name == "product_2"
    assert product_3.name == "product_3"


@pytest.mark.django_db
def test_create_categories(category_1, category_2):
    """Проверка создания объекта автора."""
    assert Category.objects.count() == 2
    assert category_1.name == "Category 1"
    assert category_2.name == "Category 2"


@pytest.mark.django_db
def test_delete_products(product_delete):
    """Проверка удаления продукта."""
    assert Product.objects.filter(id=product_delete.id).count() == 1
    product_delete.delete()
    assert Product.objects.filter(id=product_delete.id).count() == 0


@pytest.mark.django_db
def test_delete_category(category_delete):
    """Проверка удаления категории."""
    assert Category.objects.filter(id=category_delete.id).count() == 1
    category_delete.delete()
    assert Category.objects.filter(id=category_delete.id).count() == 0
