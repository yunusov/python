import pytest
from store_app.forms import ProductForm, ProductEditForm, CategoryForm


@pytest.mark.django_db
def test_product_form(category_1):
    """Тест формы создания продукта"""
    form_data = {
        "name": "Test Product",
        "description": "Test Product Descr",
        "price": 100,
        "category": category_1.id,
    }
    form = ProductForm(data=form_data)
    assert form.is_valid() == True


@pytest.mark.django_db
def test_product_edit_form(product_2, category_2):
    """Тест формы редактирования продукта"""
    form_data = {
        "name": "Test Product PEF",
        "description": "Test Product Descr PEF",
        "price": 1000,
        "category": category_2.id,
    }
    form = ProductEditForm(data=form_data, instance=product_2)
    assert form.is_valid() == True
    assert form.save().name == "Test Product PEF"


@pytest.mark.django_db
def test_category_form():
    """Тест формы создания категории"""
    form_data = {
        "name": "Test Category",
        "description": "Test Category Descr",
    }
    form = CategoryForm(data=form_data)
    assert form.is_valid() == True
