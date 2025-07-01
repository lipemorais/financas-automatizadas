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
	@if ! [ -f .env ]; then cp .env.example .env; echo "❗ NEXT STEP - fill in .env file with API credentials"; fi
	@if ! [ -f accounts.yml ]; then cp accounts.yml.example accounts.yml; echo "❗ NEXT STEP - fill in accounts.yml file with bank account IDs"; fi

s: setup
