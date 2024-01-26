.PHONY: help
.DEFAULT_GOAL := help

# auto-populate help from comments in Makefile
# source: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean:
	rm -rf .venv/

poetry-update: ## Update dependencies in pyproject.toml
	poetry update

install-dev: ## Install development dependencies
	poetry config virtualenvs.in-project true
	poetry install

style: ## Run pre-commit hooks that check code style
	poetry run pre-commit run --hook-stage manual --all-files


pytest-cov: ## Run pytest with coverage
	poetry run pytest --cov-report term --cov=statsframe tests/

build: pytest-cov ## Build the package
	poetry build

# docs: https://python-poetry.org/docs/libraries#packaging
# docs: https://python-poetry.org/docs/repositories/#configuring-credentials
publish: ## Publish the package to PyPI
	poetry publish --build

docs-build:  ## Build the docs
	poetry run quartodoc build --config docs/_quarto.yml
	poetry run pre-commit
	touch .docs-build

docs-watch:	## Build the docs and watch for changes
	poetry run quartodoc build --watch --config docs/_quarto.yml

docs-preview: docs-build ## Preview the docs
	quarto preview docs
