from django.core.management.base import BaseCommand
from faker import Faker

import random

from store_app.models import Product, Category


class Command(BaseCommand):
    help = "Генерация тестовых данных"

    def handle(self, *args, **kwargs):
        """Выполняет создание тестовых данных."""
        self.stdout.write("Начинаем генерацию.")

        fake = Faker()

        # Генерация Category
        category = []
        for i in range(5):
            cat = Category.objects.create(
                name=fake.catch_phrase(),
                description=fake.sentences(
                    nb=random.randint(3, 10),
                ),
            )
            category.append(cat)

            # Генерация Products
            products = []
            for i in range(random.randint(10, 30)):
                product = Product.objects.create(
                    name=fake.word().capitalize(),
                    description=fake.sentences(nb=random.randint(3, 10)),
                    price=random.randint(100, 10000),
                    category=cat,
                )
                products.append(product)

            self.stdout.write(f"Завершили создание {len(products)} products.")

        self.stdout.write(f"Завершили создание {len(category)} category.")

        self.stdout.write("Закончили генерацию.")
