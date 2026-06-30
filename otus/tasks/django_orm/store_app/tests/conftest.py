import pytest
from config.celery import app
from store_app.models import Category, Product


@pytest.fixture
def category_1():
    return Category.objects.create(name="Category 1")


@pytest.fixture
def category_2():
    return Category.objects.create(name="Category 2")


@pytest.fixture
def category_delete():
    return Category.objects.create(name="category_delete")


@pytest.fixture
def product_1(category_1):
    return Product.objects.create(
        name="product_1",
        description="product_1",
        price=50,
        category=category_1,
    )


@pytest.fixture
def product_2(category_1):
    return Product.objects.create(
        name="product_2",
        description="product_2",
        price=150,
        category=category_1,
    )


@pytest.fixture
def product_3(category_2):
    return Product.objects.create(
        name="product_3",
        description="product_3",
        price=1150,
        category=category_2,
    )


@pytest.fixture
def product_delete(category_2):
    return Product.objects.create(
        name="product_delete",
        description="product_delete",
        price=1150,
        category=category_2,
    )


@pytest.fixture
def celery_test_app():
    """Fixture to create a Celery app in test mode."""
    app.conf.update(
        task_always_eager=True,
        task_eager_propagates=True,
    )  # Run tasks synchronously
    return app
