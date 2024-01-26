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

# docs: https://python-poetry.org/docs/libraries#packaging
# docs: https://python-poetry.org/docs/repositories/#configuring-credentials
publish: style build
	poetry publish


docs-build:
	poetry run quartodoc build --config docs/_quarto.yml

docs-watch:
	poetry run quartodoc build --watch --config docs/_quarto.yml

docs-preview:
	quarto preview docs

