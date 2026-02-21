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

# Создаем виртуальное окружение
RUN python -m venv /opt/venv
# Активируем виртуальное окружение для последующих команд
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim as runtime

# Создаем пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Только runtime библиотека для Postgres
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Копируем виртуальное окружение из builder с правильными правами
COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv

# Настраиваем окружение
# Добавляем путь к бинарникам venv в начало PATH
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копируем код приложения с правильными правами
COPY --chown=appuser:appuser ./src ./src

USER appuser

# Default command (переопределяется в docker-compose)
CMD ["python", "-m", "src.core.main"]