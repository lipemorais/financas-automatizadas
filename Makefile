tests:
	pytest

test: tests

t: tests

run:
# 	python core/manage.py runserver

r: run

setup:
	pipenv install --dev
	pipenv run make tests
	pipenv shell

s: setup
