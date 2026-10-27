import logging

log = logging.getLogger("gunicorn.error")

def child_exit(server, worker):
    """Вызывается при остановке воркера (2 аргумента!)."""
    log.info(f"Worker {worker.pid} shutting down...")

def on_reload(server):
    """Вызывается при hot-reload (1 аргумент)."""
    log.info("Reloading application...")

# Таймауты для graceful shutdown
graceful_timeout = 120
timeout = 120
max_requests = 1000
max_requests_jitter = 50
