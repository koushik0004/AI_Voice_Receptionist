SHELL := /bin/sh

ifneq (,$(wildcard .env))
include .env
endif

DEFAULT_PYTHON := $(shell if command -v python3.13 >/dev/null 2>&1; then echo python3.13; elif command -v python3.12 >/dev/null 2>&1; then echo python3.12; elif command -v python3.11 >/dev/null 2>&1; then echo python3.11; else echo python3; fi)
PYTHON ?= $(DEFAULT_PYTHON)
VENV_DIR ?= .venv
VENV_PY := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip

HOST ?= 127.0.0.1
PORT ?= 4001
APP_MODULE ?= app.main:app

.PHONY: help setup install install-dev run dev test health clean shell

help: ## Show available commands
	@printf "\nAvailable targets:\n"
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-14s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@printf "\nCommon overrides:\n"
	@printf "  make dev PORT=4001\n"
	@printf "  make run HOST=0.0.0.0 PORT=4001\n"
	@printf "  make setup\n"
	@printf "  make setup PYTHON=python3.13\n\n"

check-python: ## Verify that the selected Python interpreter is supported
	@$(PYTHON) -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' || \
		{ printf "\nError: %s is %s, but this project requires Python >= 3.11.\n" "$$(command -v $(PYTHON) || printf $(PYTHON))" "$$($(PYTHON) --version 2>&1)"; \
		  printf "Use a Python 3.11+ interpreter, for example:\n  make setup PYTHON=python3.13\n\n"; \
		  exit 1; }

$(VENV_PY):
	$(PYTHON) -m venv $(VENV_DIR)

setup: check-python $(VENV_PY) install-dev ## Create the virtualenv and install dev dependencies

install: check-python $(VENV_PY) ## Install runtime dependencies into the virtualenv
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -e .

install-dev: check-python $(VENV_PY) ## Install runtime and development dependencies
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
