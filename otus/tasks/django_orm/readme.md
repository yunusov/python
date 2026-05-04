Описание/Пошаговая инструкция выполнения домашнего задания:
Создать Django проект и приложение:
Настроить новый проект Django.
Добавить приложение (например, store).
Создать модели:
Модель Product с полями: name, description, price, created_at.
Модель Category с полями: name, description.
Связать Product с Category через ForeignKey.
Выполнить миграции:
Создать и применить миграции.
Работа с ORM:
Создать записи для моделей, используя кастомную команду.

Критерии оценки:
Создание проекта и настройка моделей.


Загрузка:
Перед началом работы сохраните директорию со всем содержимым https://downgit.github.io/#/home?url=https://github.com/yunusov/python/tree/master/otus/tasks/django_orm на диск.

Запуск:
Перед запуском необходимо задать параметры в файле django_orm/config/.env:

SECRET_KEY=\<your secret key. Any string.\>

DEBUG=\<Is debug mode or prod? True or False\>

ENGINE=\<DB engine\>

NAME=\<DB name\>

USER=\<DB user\>

PASSWORD=\<DB password\>

HOST=\<DB localhost\>

PORT=\<DB port\>


После этого запустить start.bat.
