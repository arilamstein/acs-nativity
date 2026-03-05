.PHONY: check help

check:
	uv run ruff format .
	uv run ruff check .
	uv run mypy .

help:
	@echo "Available commands:"
	@echo "  make check          Run all CI checks (linting, type checks)"
