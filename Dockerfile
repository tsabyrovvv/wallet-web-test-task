# Dockerfile
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Применяем миграции
RUN python manage.py migrate

# Инициализация предустановленных данных
RUN python manage.py initial_data

# Указываем порт, который будет прослушивать контейнер
EXPOSE 8000

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]