tests:
	pytest

test: tests

t: tests

run:
	PYTHONPATH=$$PWD python financas_automatizadas/main.py

r: run

setup:
	pipenv install --dev
	pipenv run make tests
	pipenv shell

s: setup
