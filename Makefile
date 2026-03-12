UV ?= uv

.PHONY: help sync test lint format check module-01 module-02 module-03 module-04 module-05 module-06

help:
	@echo "Comandos disponibles:"
	@echo "  make sync       - Instala dependencias del repo completo"
	@echo "  make test       - Ejecuta la suite unificada"
	@echo "  make lint       - Ejecuta ruff check"
	@echo "  make format     - Ejecuta ruff format"
	@echo "  make check      - Compila modulos Python clave"
	@echo "  make module-01  - Ejecuta tests del modulo 01"
	@echo "  make module-02  - Ejecuta tests del modulo 02"
	@echo "  make module-03  - Ejecuta tests del modulo 03"
	@echo "  make module-04  - Ejecuta tests del modulo 04"
	@echo "  make module-05  - Ejecuta tests del modulo 05"
	@echo "  make module-06  - Ejecuta tests del modulo 06"

sync:
	$(UV) sync --extra dev

test:
	$(UV) run python -m pytest

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

check:
	$(UV) run python -m compileall 01-Introduction_AI_Engineering 03-agents/05_llmops/src

module-01:
	$(MAKE) -C 01-Introduction_AI_Engineering test-all

module-02:
	$(MAKE) -C 02-vector_data_bases test

module-03:
	$(MAKE) -C 03-agents test

module-04:
	$(MAKE) -C 04-deep_learning test

module-05:
	$(MAKE) -C 05-fastapi test

module-06:
	$(MAKE) -C 06-langgraph test
