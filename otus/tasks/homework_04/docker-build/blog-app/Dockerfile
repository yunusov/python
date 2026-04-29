FROM python:3.14.3-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.11.3 /uv /bin

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
# RUN uv sync --no-dev
ENV UV_NO_DEV=1 
ENV UV_LOCKED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project
ENV PATH="/app/.venv/bin:$PATH"

COPY . ./
