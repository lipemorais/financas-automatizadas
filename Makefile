tests:
	pytest

test: tests

t: tests

run:
	uv run python financas_automatizadas/main.py

r: run

setup:
	# We suppress the printing of each command so the user doesn't get confused, especially with the "NEXT STEP" output
	@echo "Setting up venv..."
	@uv venv
	@echo "Copying configuration files if they don't already exist..."
	@if ! [ -f .env ]; then cp .env.example .env; echo "❗ NEXT STEP - fill in .env file, using comments in file for guidance"; fi

s: setup
