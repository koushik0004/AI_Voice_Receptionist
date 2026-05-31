SHELL := /bin/sh

PYTHON ?= python3
VENV_DIR ?= .venv
VENV_PY := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip

HOST ?= 127.0.0.1
PORT ?= 8000
APP_MODULE ?= app.main:app

.PHONY: help setup install install-dev run dev test health clean shell

help: ## Show available commands
	@printf "\nAvailable targets:\n"
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-14s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@printf "\nCommon overrides:\n"
	@printf "  make dev PORT=8001\n"
	@printf "  make run HOST=0.0.0.0 PORT=8000\n"
	@printf "  make setup PYTHON=python3.11\n\n"

$(VENV_PY):
	$(PYTHON) -m venv $(VENV_DIR)

setup: $(VENV_PY) install-dev ## Create the virtualenv and install dev dependencies

install: $(VENV_PY) ## Install runtime dependencies into the virtualenv
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -e .

install-dev: $(VENV_PY) ## Install runtime and development dependencies
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -e ".[dev]"

run: ## Start the API server without auto-reload
	$(VENV_PY) -m uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT)

dev: ## Start the API server with hot reloading
	$(VENV_PY) -m uvicorn $(APP_MODULE) --reload --host $(HOST) --port $(PORT)

test: ## Run the test suite
	$(VENV_PY) -m pytest

health: ## Check the local health endpoint
	curl -fsS http://$(HOST):$(PORT)/health

shell: ## Open a shell with the virtualenv activated
	. $(VENV_DIR)/bin/activate && exec $${SHELL:-/bin/sh}

clean: ## Remove virtualenv and Python cache files
	rm -rf $(VENV_DIR) .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
