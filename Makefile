install:
	poetry install

test:
	poetry run pytest tests

test-coverage:
	poetry run pytest --cov=page_loader tests/ --cov-report xml

lint:
	poetry run flake8 page_loader tests

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

.PHONY: page_loader