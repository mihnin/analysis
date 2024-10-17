import streamlit as st
import os
import logging
from datetime import datetime
from pathlib import Path
 
def setup_logger(log_level=logging.INFO):
    # Настраивает и возвращает логгер
    logging.basicConfig(
        filename='application.log',  # Имя файла для логов
        level=log_level,  # Уровень логирования (настраиваемый)
        format='%(asctime)s UTC+00:00 - %(levelname)s - %(action)s - %(message)s',  # Формат записи логов
        datefmt = '%Y-%m-%d %H:%M:%S' # Формат времени
    )
    logger = logging.getLogger(__name__)
    return logger

def log_user_action(action, message, level="INFO"):
    # Преобразование текстового значения уровня в уровень логирования
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    # Если передан неверный уровень логирования, устанавливаем INFO по умолчанию
    log_level = log_levels.get(level.upper(), logging.INFO)
    extra = {
        'action': action
    }
    # Логирование с использованием определенного уровня
    st.session_state['logger'].log(log_level, message, extra=extra)

def create_private_download_button():
    SECRET_CODE = "log"
    # Появляется поле для ввода кода
    entered_code = st.text_input("Введите код для доступа к логам", type="password")
    # Проверяем правильность кода
    if entered_code == SECRET_CODE:
        st.success("Код верный. Кнопка для скачивания доступна.")
        # Зашитый путь к файлу
        file_path = 'application.log'
        # Преобразуем путь в объект Path
        file = Path(file_path)
        # Проверяем, существует ли файл
        if file.exists():
            # Читаем содержимое файла
            with file.open('r', encoding='latin-1') as f:
                file_content = f.read()
            # Текущая дата и время
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            # Разбираем имя файла на базовое имя и расширение
            base_name, extension = os.path.splitext(file.name)
            # Показываем кнопку для скачивания лог-файла, если код правильный
            st.download_button(
                label="Скачать лог-файл",
                data=file_content,
                file_name=f'{base_name}_{current_time}_UTC+00:00{extension}',
                mime='text/plain'
            )
        else:
            st.error("Лог-файл не найден.")
    elif entered_code:
        st.error("Неверный код. Попробуйте снова.")
