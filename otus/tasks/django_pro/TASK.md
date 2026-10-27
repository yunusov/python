Домашнее задание
Django tutorial

Цель:
пройти tutorial по Django, при этом сделав из него production-ready проект.


Описание/Пошаговая инструкция выполнения домашнего задания:
Домашнее задание включает два шага:

Пройти официальный Django tutorial и реализовать веб-сервис для блоггинга:

модели постов, пользователей, комментариев;
CRUD операции через ORM и Views;
URL маршрутизация и шаблоны;
покрытие проекта тестами.
Сделать проект production-ready, применяя рекомендации лекции:

12 factor apps, разделение настроек по средам;
логирование, static/media файлы;
развертывание через Docker, Gunicorn/Nginx;
использование environment variables.
Структура проекта
blog_project/
├── blog_app/         # models.py, views.py, urls.py, tests.py, templates/
├── blog_project/     # settings/, urls.py, wsgi.py, asgi.py
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── README.md