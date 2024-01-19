
poetry-install:
	poetry config virtualenvs.in-project true
	poetry install

hooks-all:
	poetry run pre-commit run --all-files
