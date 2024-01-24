.PHONY: docs

install-dev:
	poetry config virtualenvs.in-project true
	poetry install

style:
	poetry run pre-commit run --hook-stage manual --all-files

pytest-cov:
	poetry run pytest --cov-report term --cov=pydatasummary tests/

build: pytest-cov
	poetry build

publish: build
	poetry publish
