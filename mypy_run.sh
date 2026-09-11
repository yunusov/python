#!/usr/bin/env bash
#
# mypy_run.sh — pre-commit hook (entry: ./mypy_run.sh)
# pass_filenames: false — скрипт сам выбирает цели для проверки.
#
set -euo pipefail

# pre-commit запускает хук из корня git-репозитория, но подстрахуемся:
cd "$(git rev-parse --show-toplevel)"

# --- 1. Выбор интерпретатора ---------------------------------------------
# Приоритет: venv проекта log_analyzer (там установлен mypy), затем python из PATH.
PY="python"
for cand in \
    "otus/tasks/log_analyzer/.venv/Scripts/python"   \
    "otus/tasks/log_analyzer/.venv/bin/python"
do
    if [ -x "$cand" ]; then
        PY="$cand"
        break
    fi
done

# --- 2. Цели проверки (существующие пути) --------------------------------
TARGETS=()
for t in \
    "otus/tasks/log_analyzer/src"          \
    "otus/tasks/log_analyzer/test"
do
    [ -e "$t" ] && TARGETS+=("$t")
done

if [ ${#TARGETS[@]} -eq 0 ]; then
    echo "mypy_run.sh: нет целей для проверки — выходим."
    exit 0
fi

# --- 3. Запуск ------------------------------------------------------------
echo ">> mypy (via $PY): ${TARGETS[*]}"
exec "$PY" -m mypy "${TARGETS[@]}"
