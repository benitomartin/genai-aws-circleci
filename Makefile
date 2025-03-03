# Makefile

.PHONY: test clean ruff all help 


test: ## Run tests
	@echo "Running tests..."
	uv run pytest
	@echo "Tests complete."

ruff: ## Run Ruff linter
	@echo "Running Ruff linter..."
	ruff check . --fix --exit-non-zero-on-fix --show-fixes
	@echo "Ruff linter complete."

clean: ## Clean up cached generated files
	@echo "Cleaning up generated files..."
	find . -type d \( -name "__pycache__" -o -name ".ruff_cache" -o -name ".pytest_cache" \) -exec rm -rf {} +
	@echo "Cleanup complete."

all: ruff test clean ## Run all checks

help: ## Display this help message
	@echo "Default target: $(.DEFAULT_GOAL)"
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


.DEFAULT_GOAL := help