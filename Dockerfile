# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

# Устанавливаем инструменты сборки
# build-essential включает gcc, make и прочее для сборки C-extensions (Pandas, Numpy)
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim as runtime

# Создаем пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Только runtime библиотека для Postgres
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Копируем пакеты Python
COPY --from=builder /root/.local /home/appuser/.local

# Настраиваем окружение
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копируем код приложения
COPY ./src ./src

# Права доступа (на всякий случай)
RUN chown -R appuser:appuser /app

USER appuser

# Default command (переопределяется в docker-compose)
CMD ["python", "-m", "src.core.main"]