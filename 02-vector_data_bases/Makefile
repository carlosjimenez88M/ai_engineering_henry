UV ?= uv
PYTHON ?= python3
VENV ?= .venv
VENV_PY ?= $(VENV)/bin/python

.PHONY: install sync sync-pip lint format test run-notebook run-batman-module

install: sync

sync:
	$(UV) sync || $(MAKE) sync-pip

sync-pip:
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PY) -m pip install -e .[dev]

lint:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m ruff check .

format:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m ruff format .

test:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m pytest

run-notebook:
	$(MAKE) run-batman-module

run-batman-module:
	@test -x $(VENV_PY) || $(MAKE) sync
	mkdir -p .cache/matplotlib
	MPLCONFIGDIR=$$(pwd)/.cache/matplotlib XDG_CACHE_HOME=$$(pwd)/.cache $(VENV_PY) tools/execute_notebooks.py
