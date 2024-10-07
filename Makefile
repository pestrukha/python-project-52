install:
	poetry install

dev:
	poetry run python3 manage.py runserver

lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application
