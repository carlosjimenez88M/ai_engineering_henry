UV ?= uv

.PHONY: help check-uv venv sync sync-legacy test test-cov run-examples run-pydantic clean

help:
	@echo "Targets disponibles en python_extra_class:"
	@echo "  make venv         - Crea .venv con uv"
	@echo "  make sync         - Instala dependencias desde pyproject.toml"
	@echo "  make sync-legacy  - Instala dependencias desde requirements.txt"
	@echo "  make test         - Ejecuta test suite completa"
	@echo "  make test-cov     - Ejecuta tests con cobertura"
	@echo "  make run-examples - Ejecuta ejemplos 01..07"
	@echo "  make run-pydantic - Ejecuta ejemplo de pydantic"
	@echo "  make clean        - Limpia caches y artefactos"

check-uv:
	@command -v $(UV) >/dev/null 2>&1 || (echo "uv no esta instalado. Revisa 00_setup/README.md"; exit 1)

venv: check-uv
	$(UV) venv

sync: check-uv
	$(UV) sync

sync-legacy: check-uv
	$(UV) venv
	$(UV) pip install -r requirements.txt

test: check-uv
	$(UV) run pytest -q

test-cov: check-uv
	$(UV) run pytest --cov=03_ejercicios_leetcode --cov=04_ejemplos_runnable --cov-report=term-missing

run-examples: check-uv
	$(UV) run python 04_ejemplos_runnable/ejemplo_01_excepciones.py
	$(UV) run python 04_ejemplos_runnable/ejemplo_02_context_managers.py
	$(UV) run python 04_ejemplos_runnable/ejemplo_03_generadores.py
	$(UV) run python 04_ejemplos_runnable/ejemplo_04_logging_basico.py
	$(UV) run python 04_ejemplos_runnable/ejemplo_05_logging_avanzado.py
	$(UV) run python 04_ejemplos_runnable/ejemplo_06_comprehension_performance.py
	$(UV) run python 04_ejemplos_runnable/ejemplo_07_pydantic_ai.py

run-pydantic: check-uv
	$(UV) run python 04_ejemplos_runnable/ejemplo_07_pydantic_ai.py

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov .venv
	rm -f 04_ejemplos_runnable/*.log 04_ejemplos_runnable/*.log.*
