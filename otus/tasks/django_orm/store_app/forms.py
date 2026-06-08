from django import forms
from django.core.exceptions import ValidationError

from store_app.models import Category, Product


class ProductForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        label="Название продукта",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите название",
            }
        ),
    )
    description = forms.CharField(
        label="Описание",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите описание",
                "rows": "5",
            }
        ),
    )
    price = forms.FloatField(
        min_value=5,
        label="Цена",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категория",
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "price", "category")
        labels = {
            "name": "Название продукта",
            "description": "Описание продукта",
            "price": "Цена",
            "category": "Категория",
        }
        widget = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите описание",
                    "rows": "5",
                }
            ),
            "price": forms.NumberInput(
                {
                    "class": "form-control",
                }
            ),
            "category": forms.Select(
                {
                    "class": "form-control",
                }
            ),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 5:
            raise ValidationError("Цена не может быть меньше 5")
        return price
    
    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3:
            raise ValidationError("Название продукта должно быть более 3 символов")
        return name


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "description")
        labels = {
            "name": "Название продукта",
            "description": "Описание продукта",
        }
        widget = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите описание",
                    "rows": "5",
                }
            ),
        }
