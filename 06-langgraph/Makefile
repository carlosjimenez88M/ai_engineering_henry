UV ?= uv
MODULE_DIR := $(shell pwd)

.PHONY: help install sync lint format test test-unit test-integration \
        api-dev api-docker api-docker-down data-validate doctor smoke-test \
        notebooks-01 notebooks-02 notebooks-03 notebooks-04 \
        notebooks-05 notebooks-06 notebooks-07 notebooks-08 notebooks-all

help:
	@echo "=== Cultural Intelligence — LangGraph Module ==="
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install all dependencies (including dev)"
	@echo "  make sync             Sync dependencies"
	@echo ""
	@echo "Code quality:"
	@echo "  make lint             Run ruff check"
	@echo "  make format           Run ruff format"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run all tests"
	@echo "  make test-unit        Run unit tests only"
	@echo "  make test-integration Run integration tests (mocked, no real API)"
	@echo ""
	@echo "API:"
	@echo "  make api-dev          Start API with hot reload on port 8006"
	@echo "  make api-docker       Build and start Docker services"
	@echo "  make api-docker-down  Stop Docker services"
	@echo ""
	@echo "Data:"
	@echo "  make data-validate    Print count + first item of each JSON dataset"
	@echo ""
	@echo "Notebooks:"
	@echo "  make notebooks-01     Execute notebook 01"
	@echo "  make notebooks-all    Execute all notebooks"
	@echo ""
	@echo "Health:"
	@echo "  make doctor           Validate environment setup"
	@echo ""
	@echo "Smoke test:"
	@echo "  make smoke-test       End-to-end test with real LLM (requires OPENAI_API_KEY)"

install:
	$(UV) sync --extra dev

sync:
	$(UV) sync --extra dev

lint:
	$(UV) run ruff check src/ tests/

format:
	$(UV) run ruff format src/ tests/

test:
	$(UV) run pytest tests/ -v --tb=short

test-unit:
	$(UV) run pytest tests/unit/ -v --tb=short

test-integration:
	$(UV) run pytest tests/integration/ -v --tb=short

api-dev:
	PYTHONPATH=src $(UV) run uvicorn cinematic_intelligence.api.main:app \
		--reload \
		--host 0.0.0.0 \
		--port 8006

api-docker:
	docker compose -f docker/docker-compose.yml up --build -d

api-docker-down:
	docker compose -f docker/docker-compose.yml down

data-validate:
	@echo "=== Validating datasets ==="
	@$(UV) run python -c "import json,pathlib; d=json.loads(pathlib.Path('00_datos/nolan_films.json').read_text('utf-8')); print(f'nolan_films.json: {len(d)} items | first: {d[0][\"titulo\"]} ({d[0][\"año\"]})')"
	@$(UV) run python -c "import json,pathlib; d=json.loads(pathlib.Path('00_datos/king_books.json').read_text('utf-8')); print(f'king_books.json: {len(d)} items | first: {d[0][\"titulo\"]} ({d[0][\"año_publicacion\"]})')"
	@$(UV) run python -c "import json,pathlib; d=json.loads(pathlib.Path('00_datos/davis_albums.json').read_text('utf-8')); print(f'davis_albums.json: {len(d)} items | first: {d[0][\"titulo\"]} ({d[0][\"año\"]})')"

doctor:
	@echo "=== Environment Doctor ==="
	@$(UV) run python -c "\
import os, sys; \
key = os.getenv('OPENAI_API_KEY', ''); \
print('OPENAI_API_KEY:', 'SET' if key and not key.startswith('sk-test') else 'MISSING or test key'); \
print('Python:', sys.version); \
import langgraph; print('langgraph:', langgraph.__version__); \
import langchain; print('langchain:', langchain.__version__); \
import fastapi; print('fastapi:', fastapi.__version__); \
"

smoke-test:  ## Run end-to-end smoke test with real LLM (requires OPENAI_API_KEY)
	$(UV) run python scripts/smoke_test.py

notebooks-01:
	$(UV) run jupyter nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=120 \
		01_estado_y_grafos/01_estado_y_grafos.ipynb \
		--output 01_estado_y_grafos/01_estado_y_grafos_executed.ipynb

notebooks-02:
	$(UV) run jupyter nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=120 \
		02_mensajes_y_llm/02_mensajes_y_llm.ipynb \
		--output 02_mensajes_y_llm/02_mensajes_y_llm_executed.ipynb

notebooks-03:
	$(UV) run jupyter nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=120 \
		03_herramientas/03_herramientas.ipynb \
		--output 03_herramientas/03_herramientas_executed.ipynb

notebooks-04:
	$(UV) run jupyter nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=180 \
		04_enrutamiento_condicional/04_enrutamiento_condicional.ipynb \
		--output 04_enrutamiento_condicional/04_enrutamiento_condicional_executed.ipynb

notebooks-05:
	$(UV) run jupyter nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=120 \
		05_salida_estructurada/05_salida_estructurada.ipynb \
		--output 05_salida_estructurada/05_salida_estructurada_executed.ipynb

notebooks-06:
	$(UV) run jupyter nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=120 \
		06_memoria_y_checkpointing/06_memoria_y_checkpointing.ipynb \
		--output 06_memoria_y_checkpointing/06_memoria_y_checkpointing_executed.ipynb

notebooks-07:
	$(UV) run jupyter nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=180 \
		07_paralelizacion/07_paralelizacion.ipynb \
		--output 07_paralelizacion/07_paralelizacion_executed.ipynb

notebooks-08:
	$(UV) run jupyter nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=300 \
		08_sistema_multiagente/08_sistema_multiagente.ipynb \
		--output 08_sistema_multiagente/08_sistema_multiagente_executed.ipynb

notebooks-all: notebooks-01 notebooks-02 notebooks-03 notebooks-04 \
               notebooks-05 notebooks-06 notebooks-07 notebooks-08
	@echo "=== All notebooks executed successfully ==="
