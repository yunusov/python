from django.contrib import admin

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "category_name",
        "created_at",
    )

    class CategoryNameFilter(admin.SimpleListFilter):
        title = "Имя категории"
        parameter_name = "category_name"

        def lookups(self, request, model_admin):
            return [(cat.name, cat.name) for cat in Category.objects.all()]

        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(category__name=self.value())
            return queryset

    list_filter = (CategoryNameFilter, "created_at")

    @admin.display(description="Category") 
    def category_name(self, obj):
        return obj.category.name
    
    @admin.action(description="Увеличить цену на 10")
    def increase_price(self, request, queryset):
        for product in queryset:
            product.price += 10
            product.save()

    actions = ("increase_price",)
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description") 
    search_fields = ("name",)
    search_help_text = "Поиск по имени категории"
 

admin.site.site_header = "Админ панель магазина"
