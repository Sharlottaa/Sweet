@echo off
:loop

REM Запускаем скрипт Python
"D:\Shop\venv\Scripts\python.exe" "D:\Shop\backup_script.py"

REM Ждем 60 секунд (1 минута) перед следующим запуском
timeout /t 1800

REM Повторяем цикл
goto loop
