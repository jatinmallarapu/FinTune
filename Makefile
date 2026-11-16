# Run the fintune example with the same inputs documented in the quickstart.
.PHONY: dev test lint

dev:
	python fintune.py baseline examples/synthetic.json

test:
	python -m pytest --cov=fintune --cov-fail-under=70

lint:
	ruff check .
	ruff format --check .
	mypy fintune.py
