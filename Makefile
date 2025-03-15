.PHONY: format test

format:
	black -l 120 .
	isort .

test:
	python manage.py test