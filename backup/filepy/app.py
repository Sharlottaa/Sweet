from routers import *
from config import *
import os
import subprocess
from datetime import datetime

import subprocess
import os
import json
import subprocess
from datetime import datetime


def backup_database():
    db_user = 'postgres'
    db_password = 'rootroot'
    db_name = 'postgres'
    db_host = '127.0.0.1'

    # Устанавливаем переменные окружения для аутентификации
    os.environ['PGUSER'] = db_user
    os.environ['PGPASSWORD'] = db_password
    os.environ['PGHOST'] = db_host

    # Полный путь к исполняемому файлу pg_dump
    pg_dump_executable = "C:\\Program Files\\PostgreSQL\\16\\bin\\pg_dump.exe"

    # Команда для создания резервной копии схемы
    schema_backup_file = f'schema_backup_{db_name}_{datetime.now().strftime("%Y%m%d%H%M%S")}.sql'
    schema_command = [
        pg_dump_executable, "-s", "-f", schema_backup_file, db_name
    ]
    subprocess.run(schema_command, check=True)

    # Команда для создания резервной копии данных в формате SQL
    data_backup_file = f'data_backup_{db_name}_{datetime.now().strftime("%Y%m%d%H%M%S")}.sql'
    data_command = [
        pg_dump_executable, "-d", db_name, "-f", data_backup_file
    ]

    try:
        # Выполнение команды для создания SQL-дампа
        result = subprocess.run(data_command, check=True, capture_output=True, text=True)
        print(f'Stdout: {result.stdout}')
        print(f'Stderr: {result.stderr}')
    except subprocess.CalledProcessError as e:
        print(f'An error occurred: {e.stderr}')


if __name__ == "__main__":
    with app.app_context():  # Активация контекста приложения
        db.create_all()  # Создание табли

        app.run()  # Запуск приложения
    backup_database()
