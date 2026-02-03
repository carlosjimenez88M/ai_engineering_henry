UV ?= uv
PYTHON ?= python3

.PHONY: check-uv install run-ai run-ai-context run-ai-model run-se test-se test-ai test-ai-cov test-all lint format check clean

check-uv:
	@command -v $(UV) >/dev/null 2>&1 || (echo "uv no esta instalado. Instala uv y vuelve a ejecutar."; exit 1)

install: check-uv
	$(UV) sync

run-ai: check-uv
	$(UV) run python 01_class/ai_engineering/brief_builder/main.py

run-ai-context: check-uv
	$(UV) run python 01_class/ai_engineering/brief_builder/main.py --context "$(CONTEXT)"

run-ai-model: check-uv
	OPENAI_MODEL="$(MODEL)" $(UV) run python 01_class/ai_engineering/brief_builder/main.py

run-se: check-uv
	$(UV) run python 01_class/python_software_engineering/src/app.py

test-se: check-uv
	$(UV) run pytest 01_class/python_software_engineering/tests -q

test-ai: check-uv
	$(UV) run pytest 01_class/ai_engineering/tests -v

test-ai-cov: check-uv
	$(UV) run pytest 01_class/ai_engineering/tests --cov=01_class/ai_engineering --cov-report=html

test-all: check-uv
	$(UV) run pytest -v

lint: check-uv
	$(UV) run ruff check .

format: check-uv
	$(UV) run ruff format .

check:
	$(PYTHON) -m compileall 01_class

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
