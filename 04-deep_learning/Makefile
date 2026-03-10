UV ?= uv
VENV ?= .venv
VENV_PY ?= $(VENV)/bin/python

.PHONY: help sync kernel test lint format doctor corpus-check notebooks-smoke notebooks-all clean

help:
	@echo "Comandos disponibles en 04-deep_learning:"
	@echo "  make sync            - Instala dependencias y registra el kernel de Jupyter"
	@echo "  make kernel          - Re-registra el kernel sin reinstalar dependencias"
	@echo "  make test            - Ejecuta la suite de tests del modulo"
	@echo "  make doctor          - Reporta entorno, hardware y variables utiles"
	@echo "  make corpus-check    - Valida el corpus local de Las mil y una noches"
	@echo "  make notebooks-smoke - Ejecuta las 7 notebooks en modo reducido"
	@echo "  make notebooks-all   - Ejecuta las 7 notebooks en modo completo"
	@echo "  make lint            - Ejecuta ruff"
	@echo "  make format          - Formatea con ruff"
	@echo "  make clean           - Limpia caches, artefactos y entorno local"

sync:
	$(UV) sync --extra dev
	$(VENV_PY) -m ipykernel install --user --name henry-deep-learning --display-name "Henry Deep Learning"

kernel:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m ipykernel install --user --name henry-deep-learning --display-name "Henry Deep Learning"

test:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m pytest

doctor:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) scripts/doctor.py

corpus-check:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m tools.text_corpus

notebooks-smoke:
	@test -x $(VENV_PY) || $(MAKE) sync
	HENRY_DL_SMOKE=1 HENRY_DL_ONLINE_MODE=0 $(VENV_PY) tools/execute_notebooks.py all --smoke --timeout 1200

notebooks-all:
	@test -x $(VENV_PY) || $(MAKE) sync
	HENRY_DL_ONLINE_MODE=0 $(VENV_PY) tools/execute_notebooks.py all --timeout 1800

lint:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m ruff check .

format:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m ruff format .

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .artifacts .pytest_cache .ruff_cache .coverage htmlcov .venv
