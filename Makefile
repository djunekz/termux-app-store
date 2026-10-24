PYTHON ?= python3

.PHONY: install test coverage lint format typecheck sync-build-script check clean

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

coverage:
	$(PYTHON) -m pytest --cov=tools --cov=termux_app_store --cov-report=term-missing

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

format:
	$(PYTHON) -m ruff check --fix .
	$(PYTHON) -m ruff format .

typecheck:
	$(PYTHON) -m mypy

sync-build-script:
	cp build-package.sh termux_app_store/data/build-package.sh

check: lint typecheck test

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml htmlcov
