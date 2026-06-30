"""
Описание/Пошаговая инструкция выполнения домашнего задания:
Настроить Celery и Redis:
Установить Celery и Redis.
Подключить Redis как брокер задач для Celery.
Реализовать фоновую задачу:
Создать задачу для логирования информации о добавлении нового товара.
Задача должна выводить сообщение на консоль (например, название нового товара).
Протестировать Celery:
Убедиться, что задачи корректно ставятся в очередь и выполняются.
"""


import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
