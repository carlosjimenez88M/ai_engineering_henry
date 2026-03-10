UV ?= uv
PYTHON ?= python3
VENV ?= .venv
VENV_PY ?= $(VENV)/bin/python

.PHONY: help install sync lint format test \
        run-01 run-02 run-03 run-04 run-05 run-06 run-07 \
        test-07 docker-build docker-up docker-test docker-down

help:
	@echo "Comandos disponibles:"
	@echo "  make install      - Instala dependencias (uv sync --extra dev)"
	@echo "  make sync         - Sincroniza entorno virtual"
	@echo "  make test         - Ejecuta todos los tests (05 y 06)"
	@echo "  make lint         - Ejecuta ruff check"
	@echo "  make format       - Ejecuta ruff format"
	@echo "  make run-01       - Arranca 01_fundamentos (puerto 8001)"
	@echo "  make run-02       - Arranca 02_modelos_pydantic (puerto 8002)"
	@echo "  make run-03       - Arranca 03_todo_app_base (puerto 8003)"
	@echo "  make run-04       - Arranca 04_migraciones (puerto 8004)"
	@echo "  make run-05       - Arranca 05_testing (puerto 8005)"
	@echo "  make run-06       - Arranca 06_frontend (puerto 8006)"
	@echo "  make run-07       - Arranca 07_docker con Docker (puerto 8007)"
	@echo "  make test-07      - Ejecuta tests de 07_docker localmente (sin Docker)"
	@echo "  make docker-build - Construye la imagen Docker de 07_docker"
	@echo "  make docker-up    - Inicia la API en Docker (modo daemon)"
	@echo "  make docker-test  - Ejecuta pytest dentro del contenedor Docker"
	@echo "  make docker-down  - Detiene y elimina los contenedores Docker"

install: sync

sync:
	$(UV) sync --extra dev

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

test:
	$(UV) run pytest --override-ini="testpaths=05_testing/TodoApp/test" \
		--override-ini="pythonpath=05_testing"
	$(UV) run pytest --override-ini="testpaths=06_frontend/TodoApp/test" \
		--override-ini="pythonpath=06_frontend"

run-01:
	$(UV) run fastapi dev 01_fundamentos/books.py --port 8001

run-02:
	$(UV) run fastapi dev 02_modelos_pydantic/books2.py --port 8002

run-03:
	cd 03_todo_app_base && $(UV) run fastapi dev TodoApp/main.py --port 8003

run-04:
	cd 04_migraciones && $(UV) run fastapi dev TodoApp/main.py --port 8004

run-05:
	cd 05_testing && $(UV) run fastapi dev TodoApp/main.py --port 8005

run-06:
	cd 06_frontend && $(UV) run fastapi dev TodoApp/main.py --port 8006

run-07:
	docker-compose -f 07_docker/docker-compose.yml up api

test-07:
	cd 07_docker && PYTHONPATH=. $(UV) run pytest tests/ -v

docker-build:
	docker-compose -f 07_docker/docker-compose.yml build

docker-up:
	docker-compose -f 07_docker/docker-compose.yml up -d api

docker-test:
	docker-compose -f 07_docker/docker-compose.yml run --rm test

docker-down:
	docker-compose -f 07_docker/docker-compose.yml down
