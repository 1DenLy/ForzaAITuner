# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

# libpq-dev нужен для сборки драйверов PostgreSQL (asyncpg/psycopg2)
# gcc и python3-dev нужны для компиляции C-расширений (pandas, numpy)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости в локальную директорию
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime (итоговый легкий образ)
FROM python:3.12-slim as runtime

# Создаем не-root пользователя для безопасности
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Устанавливаем только runtime-библиотеки для Postgres (без компиляторов)
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Копируем установленные пакеты из этапа builder
COPY --from=builder /root/.local /home/appuser/.local

# Настраиваем PATH, чтобы видеть установленные пакеты
ENV PATH=/home/appuser/.local/bin:$PATH
# Запрещаем создание .pyc файлов и буферизацию вывода (важно для логов в Docker)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копируем исходный код
COPY ./src ./src

# Переключаемся на пользователя
USER appuser

# Entrypoint не указываем жестко, так как у нас разные сервисы запускаются из одного образа
CMD ["python", "-m", "src.core.main"]