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

.style:
	poetry run pre-commit run --hook-stage manual --all-files; touch .style

style: .style ## Run pre-commit hooks that check code style

.pytest-cov: .style
	poetry run pytest --cov-report term --cov=statsframe tests/
	touch .pytest-cov

pytest-cov: .pytest-cov ## Run pytest with coverage

.build: .pytest-cov ## Build the package
	poetry build
	touch .build

build: .build ## Build the package

# docs: https://python-poetry.org/docs/libraries#packaging
# docs: https://python-poetry.org/docs/repositories/#configuring-credentials
.publish: .build
	poetry publish

publish: .publish ## Publish the package to PyPI

.docs-build:
	poetry run quartodoc build --config docs/_quarto.yml
	touch .docs-build

docs-build: .docs-build ## Build the docs

docs-watch:	## Build the docs and watch for changes
	poetry run quartodoc build --watch --config docs/_quarto.yml

docs-preview: .docs-build ## Preview the docs
	quarto preview docs
