# docs: justfile docs: https://just.systems/man/en/
default:
	just --list --unsorted

# Clean environment
clean:
	rm -rf .venv/

# Update dependencies in pyproject.toml
poetry-update:
	poetry update

# Install development dependencies
install-dev:
	poetry config virtualenvs.in-project true
	poetry install

# Run pre-commit hooks that check code style
style:
	poetry run pre-commit run --hook-stage manual --all-files

# Run pytest with coverage
pytest-cov:
	poetry run pytest --cov-report term --cov=statsframe tests/

# Build the package
build: pytest-cov
	poetry build

# docs: https://python-poetry.org/docs/libraries#packaging
# docs: https://python-poetry.org/docs/repositories/#configuring-credentials
# Publish the package to PyPI
publish:
	poetry publish --build

# Build documentation and website
docs-build:
	cd docs && poetry run quartodoc build --verbose

# Build the documentation and watch for changes
docs-watch:
	poetry run quartodoc build --watch --config docs/_quarto.yml

# Render documentation and website
docs-render: docs-build
	cd docs && poetry run quarto render

# Clean docs build
docs-clean:
	rm -rf docs/_build docs/api/api_card

# Preview the docs
docs-preview: docs-build
	quarto preview docs
