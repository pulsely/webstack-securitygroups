.DEFAULT_GOAL := dev

dev:
	source ./venv/bin/activate ;  python manage.py runserver

test:
	python manage.py test

reset:
	python manage.py reset
