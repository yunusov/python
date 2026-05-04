from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    