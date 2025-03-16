.PHONY: format test

format:
	black --line-length=120 .
	isort --line-width=120 --profile=black .

test:
	python manage.py test