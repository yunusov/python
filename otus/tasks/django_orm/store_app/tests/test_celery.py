import pytest

from store_app.loguru_config import AppLogger
from store_app.tasks import send_info_email


logger = AppLogger().get_logger()

@pytest.mark.django_db(transaction=True)
def test_celery_msg(celery_test_app):
    """Проверка создания объекта"""
    task = send_info_email.delay("user@mail.ru", "Продукт создан", "123")
    assert task.successful()
    assert task.result == 'Email sent to user@mail.ru with 123'
