FROM python:3.14-slim

# deb.debian.org (Fastly CDN) недоступен из текущей сети — переключаем apt на зеркало Яндекса
RUN set -eux; \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i 's|http://deb.debian.org|http://mirror.yandex.ru|g; s|http://security.debian.org|http://mirror.yandex.ru/debian-security|g' /etc/apt/sources.list.d/debian.sources; \
    fi; \
    if [ -f /etc/apt/sources.list ]; then \
        sed -i 's|http://deb.debian.org|http://mirror.yandex.ru|g; s|http://security.debian.org|http://mirror.yandex.ru/debian-security|g' /etc/apt/sources.list; \
    fi

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential tree curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/laike9m/Python-Type-Challenges && \
    cd Python-Type-Challenges &&  \
    pip3 install -r requirements.txt && \
    pip3 install poetry==2.4.1 gunicorn

RUN sed -i '/^venvPath = /d; /^venv = /d' /Python-Type-Challenges/pyproject.toml

WORKDIR /Python-Type-Challenges

# exec-форма: флаг и значение -b должны быть отдельными аргументами
CMD ["gunicorn", "-b", "0.0.0.0:8001", "app:app"]
