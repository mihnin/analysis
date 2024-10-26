# Используем официальный образ Python для сборки зависимостей
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Открываем порт 8506
EXPOSE 8506

# Определяем команду для запуска приложения на порту 8506
CMD ["streamlit", "run", "app.py", "--server.port=8506"]
