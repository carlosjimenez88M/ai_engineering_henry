UV ?= uv
PYTHON ?= python3

.PHONY: check-uv install install-prompting run-ai run-ai-context run-ai-model run-se test-se test-ai test-ai-cov test-all lint format check run-cot run-react run-cot-pydantic run-react-pydantic run-all-prompting run-notebooks verify-notebooks clean

check-uv:
	@command -v $(UV) >/dev/null 2>&1 || (echo "uv no esta instalado. Instala uv y vuelve a ejecutar."; exit 1)

install: check-uv
	$(UV) sync

install-prompting: check-uv
	$(UV) sync

run-ai: check-uv
	$(UV) run python 01_class/ai_engineering/brief_builder/main.py

run-ai-context: check-uv
	$(UV) run python 01_class/ai_engineering/brief_builder/main.py --context "$(CONTEXT)"

run-ai-model: check-uv
	OPENAI_MODEL="$(MODEL)" $(UV) run python 01_class/ai_engineering/brief_builder/main.py

run-se: check-uv
	$(UV) run python 01_class/python_software_engineering/src/app.py

run-cot: check-uv
	@echo " Running CoT examples (JSON-based)..."
	$(UV) run python 02-prompting/COT/Notebooks/01_zero_shot_cot_recomendador.py
	$(UV) run python 02-prompting/COT/Notebooks/02_few_shot_cot_feedback_loop.py

run-react: check-uv
	@echo " Running ReAct examples (JSON-based)..."
	$(UV) run python 02-prompting/ReAct/Notebooks/01_react_agente_coqueto.py
	$(UV) run python 02-prompting/ReAct/Notebooks/02_react_personas_feedback_loop.py

run-cot-pydantic: check-uv
	@echo " Running CoT examples with Pydantic (type-safe)..."
	@if [ -f 02-prompting/COT/Notebooks/03_zero_shot_cot_pydantic.py ]; then \
		$(UV) run python 02-prompting/COT/Notebooks/03_zero_shot_cot_pydantic.py; \
	else \
		echo "  Pydantic COT examples not yet created. Run JSON examples with 'make run-cot' first."; \
	fi
	@if [ -f 02-prompting/COT/Notebooks/04_few_shot_cot_pydantic.py ]; then \
		$(UV) run python 02-prompting/COT/Notebooks/04_few_shot_cot_pydantic.py; \
	else \
		echo "  Few-shot Pydantic COT example not yet created."; \
	fi

run-react-pydantic: check-uv
	@echo " Running ReAct examples with Pydantic (type-safe)..."
	@if [ -f 02-prompting/ReAct/Notebooks/03_react_agente_pydantic.py ]; then \
		$(UV) run python 02-prompting/ReAct/Notebooks/03_react_agente_pydantic.py; \
	else \
		echo "  Pydantic ReAct examples not yet created. Run JSON examples with 'make run-react' first."; \
	fi
	@if [ -f 02-prompting/ReAct/Notebooks/04_react_personas_pydantic.py ]; then \
		$(UV) run python 02-prompting/ReAct/Notebooks/04_react_personas_pydantic.py; \
	else \
		echo "  Few-shot Pydantic ReAct example not yet created."; \
	fi

run-all-prompting: run-cot run-react run-cot-pydantic run-react-pydantic
	@echo " All prompting examples executed (JSON + Pydantic)"

run-notebooks: check-uv
	@echo " Executing Jupyter notebooks..."
	$(UV) run python 02-prompting/tools/execute_notebooks.py

verify-notebooks: run-notebooks

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
