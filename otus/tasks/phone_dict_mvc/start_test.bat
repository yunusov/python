@rem запуск тестов pytest

@rem включаем тестовую переменную
@set TEMP_APP_ENV=%APP_ENV%
@set APP_ENV=PYTEST

@cls
python -m pytest

@rem возвращаем прежнее значение
@set APP_ENV=%TEMP_APP_ENV%
@pause