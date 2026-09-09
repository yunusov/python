PROJECT_ROOT := $(realpath $(dir $(abspath $(lastword $(MAKEFILE_LIST))))..)

ENTRY_POINT ?= main-run

run:
	cd $(PROJECT_ROOT) && poetry run $(ENTRY_POINT) --config src/log_analyzer/config.json

linting:
	cd $(PROJECT_ROOT) && poetry run ruff format src test
	cd $(PROJECT_ROOT) && poetry run ruff check --fix src test

tests:
	cd $(PROJECT_ROOT) && poetry run pytest -xvvs test/

test-cov:
	cd $(PROJECT_ROOT) && poetry run pytest --cov=src --cov-report=html test/