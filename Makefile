
poetry-install:
	poetry config virtualenvs.in-project true
	poetry install

hooks-all:
	poetry run pre-commit run --all-files

pytest-cov:
	poetry run pytest --cov-report term --cov=pydatasummary tests/
