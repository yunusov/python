from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_info_email(rec_email, subject, message):
    """Фоновая задача для отправки уведомления по email."""
    send_mail(
        subject=subject,
        message=message,
        from_email='admin@mail.ru',
        recipient_list=[rec_email],
    )
    return f'Email sent to {rec_email} with {message}'
