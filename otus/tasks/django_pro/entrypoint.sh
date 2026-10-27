#!/bin/sh
set -e

# Ждём готовности PostgreSQL
until python /app/blog_project/manage.py dbshell --command "SELECT 1" 2>/dev/null || \
      python -c "import psycopg2; psycopg2.connect(dbname='blog_production', user='user', password='password', host='db', port='5432').close()" 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is up - running migrations"
python /app/blog_project/manage.py migrate

echo "Starting gunicorn with args: $@"   # <-- отладка
exec "$@"
