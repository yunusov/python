@rem Отчёт покрытия проекта тестами
@echo off

python -m pytest --cov=src --cov-report=html

choice /c YN /d N /t 10 /m "Показать отчёт покрытия тестами в браузере? (Y/N)"
if errorlevel 2 goto exit_
if errorlevel 1 echo goto report_

:report_
htmlcov\index.html
:exit_