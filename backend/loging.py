from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import logging
import os

log_directory = "logging"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)


# Настройка логирования
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

current_date = datetime.now().strftime("%Y-%m-%d")
log_file_name = f"app_{current_date}.log"


# Создаем обработчик, который будет записывать логи в файл с ежедневной ротацией
handler = TimedRotatingFileHandler(
    filename=os.path.join(log_directory, log_file_name),  # Имя файла с датой
    when="midnight",  # Ротация каждый день в полночь
    interval=1,  # Каждый день
    backupCount=7  # Хранить последние 7 файлов
)

# Форматирование логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(handler)