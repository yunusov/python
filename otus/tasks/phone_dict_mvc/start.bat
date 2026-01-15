@rem Скрипт для пользовательского старта программы "Телефонный справочник"

@echo off
@chcp 65001 > nul
echo Проверка Python...

@REM Проверка версии Python
python --version > nul 2>&1
if errorlevel 1 (
    echo Ошибка: Python не установлен или не добавлен в PATH
    echo Скачайте с https://python.org
    pause
    exit /b 1
)

pip install --upgrade pip

if exist "requirements.txt" (
    echo Установка зависимостей...
    pip install -r requirements.txt
)

python main.py
@pause