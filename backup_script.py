import yadisk
import os
from datetime import datetime

# Вставьте ваш токен здесь
token = "y0_AgAAAABzFUiEAAsPkAAAAAD2LxhVj_GPCXpZRTaNbZdbFXeqokEophg"

# Подключаемся к Яндекс.Диску
y = yadisk.YaDisk(token=token)

# Путь к папке, которую хотите забэкапить
backup_folder = "D:\\shop\\backup"

# Создаем уникальное и красивое имя папки с текущей датой и временем
# Формат: "Backup1_2023-12-28_15-30-00"
# Создаем уникальное и красивое имя папки с текущей датой и временем
backup_time = datetime.now().strftime("Backup_%Y-%m-%d_%H-%M-%S")
remote_backup_folder = "disk:/" + backup_time  # Добавляем префикс "disk:/"

# Проверяем, подключен ли Яндекс.Диск
if not y.check_token():
    print("Неверный токен!")
else:
    # Проходим по всем файлам и папкам в директории
    for root, dirs, files in os.walk(backup_folder):
        for file in files:
            local_path = os.path.join(root, file)
            remote_path = remote_backup_folder + "/" + os.path.relpath(local_path, backup_folder).replace("\\", "/")

            # Создаем все родительские папки для файла, если они еще не созданы
            parts = remote_path.split("/")
            path_to_create = "disk:/"
            for part in parts[1:-1]:  # пропускаем имя файла и первый слеш
                path_to_create += part + "/"
                if not y.exists(path_to_create):
                    y.mkdir(path_to_create)

            # Загружаем файлы
            with open(local_path, 'rb') as f:
                y.upload(f, remote_path)

    print("Бэкап завершен.")