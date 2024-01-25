.PHONY: docs

install-dev:
	poetry config virtualenvs.in-project true
	poetry install

style:
	poetry run pre-commit run --hook-stage manual --all-files

pytest-cov: install-dev
	poetry run pytest --cov-report term --cov=statsframe tests/

build:
	poetry build

publish: style build
	poetry publish
