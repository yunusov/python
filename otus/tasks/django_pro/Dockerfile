FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_LOCKED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/
RUN uv sync --no-install-project
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/blog_project:${PYTHONPATH}"
ENV ENVIRONMENT="production"

COPY . ./

RUN python blog_project/manage.py collectstatic --noinput

EXPOSE 8000

STOPSIGNAL SIGTERM

CMD ["gunicorn", "blog_project.blog_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--config", "gunicorn_config.py", "--graceful-timeout", "120", "--timeout", "120", "--max-requests", "1000", "--max-requests-jitter", "50", "--log-file", "-", "--access-logfile", "-"]
