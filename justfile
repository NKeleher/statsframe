# docs: justfile docs: https://just.systems/man/en/
default:
	just --list --unsorted

# Aliases
alias dev := install-dev
alias commit := git-commit
alias push-up := git-push-upstream
alias push := git-push

# Clean environment
[confirm]
clean:
	rm -rf .venv/

# Update dependencies in pyproject.toml
poetry-update:
	poetry update

# Install development dependencies
install-dev:
	poetry config virtualenvs.in-project true
	poetry install

# Install pre-commit hooks
install-hooks:
	poetry run pre-commit install --install-hooks

# Run pre-commit hooks that check code style
style: install-hooks
	poetry run pre-commit run --hook-stage manual --all-files

# Run pytest
tests:
	poetry run pytest

# Run pytest with coverage
tests-cov:
	poetry run pytest --cov-report term --cov=statsframe

# Git add file
[no-cd]
git-add file:
	poetry run git add {{file}}

# Git commit with message
git-commit m:
	poetry run git commit --no-verify -m "{{m}}"

# Git push upstream to origin
git-push-upstream b:
	poetry run git push --set-upstream origin {{b}}

# Git push
git-push:
	poetry run git push

# Build the package
build: tests
	poetry build

# docs: https://python-poetry.org/docs/libraries#packaging
# docs: https://python-poetry.org/docs/repositories/#configuring-credentials
# Publish the package to PyPI
publish:
	poetry publish --build

# Build documentation and website
docs-build:
	poetry run quartodoc build --verbose --config docs/_quarto.yml

# Render documentation and website
render: docs-build
	poetry run quarto render docs

# Build the documentation and watch for changes
docs-watch:
	poetry run poetry run quartodoc build --watch --verbose --config docs/_quarto.yml

# Preview the docs
preview:
	poetry run quarto preview docs

# Clean docs build
docs-clean:
	rm -rf docs/_build docs/api/api_card
