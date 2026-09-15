# syntax=docker/dockerfile:1

# ---------- builder: зависимости из poetry.lock ----------
FROM python:3.14-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# venv, который целиком переедет в рантайм-слой
RUN python -m venv /opt/venv

# poetry нужен только на этапе сборки
RUN pip install "poetry>=2.1,<3"

WORKDIR /app
# сначала только манифесты: слой с зависимостями кэшируется,
# пока pyproject.toml / poetry.lock не меняются
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root --no-ansi \
    && python -c "import structlog, tqdm, pre_commit; print('deps ok:', structlog.__version__)"

# ---------- runtime ----------
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
# Приложение запускаем из исходников (не ставим пакет в site-packages):
# в коде TOP_FOLDER/PARENT_FOLDER считаются от __file__, и такой способ
# сохраняет расположение шаблона report.html и статики внутри /app.
COPY src ./src
COPY config-docker.json /app/config-docker.json

ENV PYTHONPATH=/app/src

# непривилегированный пользователь
RUN useradd --create-home --shell /usr/sbin/nologin appuser
USER appuser

# точки подключения входных/выходных данных
VOLUME ["/data/logs", "/data/reports"]

ENTRYPOINT ["python", "-m", "log_analyzer.main"]
CMD ["--config", "/app/config-docker.json"]
