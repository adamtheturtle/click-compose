.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make test          - Run test suite"
	@echo "  make lint          - Run all linters"
	@echo "  make docs          - Build documentation"
	@echo "  make clean         - Clean build artifacts"

.PHONY: test
test:
	uv run --extra=dev pytest -s -vvv --cov-fail-under 100 --cov=src/ --cov=tests/ tests/

.PHONY: lint
lint:
	uv run --extra=dev pre-commit run --all-files --hook-stage pre-push

.PHONY: docs
docs:
	uv run --extra=dev sphinx-build -W docs/source/ docs/build/

.PHONY: clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf docs/build/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
