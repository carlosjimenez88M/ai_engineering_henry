UV ?= uv
PYTHON ?= python3

.PHONY: check-uv install install-prompting run-ai run-ai-context run-ai-model run-se test-se test-ai test-ai-cov test-project test-all lint format check run-cot run-react run-cot-pydantic run-react-pydantic run-all-prompting run-notebooks verify-notebooks run-cot-langchain run-react-langchain run-notebooks-langchain verify-notebooks-langchain run-langgraph-architectures run-notebooks-langgraph verify-notebooks-langgraph run-project clean

check-uv:
	@command -v $(UV) >/dev/null 2>&1 || (echo "uv no esta instalado. Instala uv y vuelve a ejecutar."; exit 1)

install: check-uv
	$(UV) sync

install-prompting: check-uv
	$(UV) sync

run-ai: check-uv
	$(UV) run python 01-introduction/ai_engineering/brief_builder/main.py

run-ai-context: check-uv
	$(UV) run python 01-introduction/ai_engineering/brief_builder/main.py --context "$(CONTEXT)"

run-ai-model: check-uv
	OPENAI_MODEL="$(MODEL)" $(UV) run python 01-introduction/ai_engineering/brief_builder/main.py

run-se: check-uv
	$(UV) run python 01-introduction/python_software_engineering/src/app.py

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

run-cot-langchain: check-uv
	@echo " Running CoT LangChain examples..."
	$(UV) run python 03_langchain_prompting/COT_LangChain/Notebooks/01_cot_langchain_avanzado.py

run-react-langchain: check-uv
	@echo " Running ReAct LangChain examples..."
	$(UV) run python 03_langchain_prompting/ReAct_LangChain/Notebooks/01_react_langchain_avanzado.py

run-notebooks-langchain: check-uv
	@echo " Executing Class 03 notebooks..."
	$(UV) run python 03_langchain_prompting/tools/execute_notebooks.py

verify-notebooks-langchain: run-notebooks-langchain

run-langgraph-architectures: check-uv
	@echo " Running LangGraph architecture examples..."
	$(UV) run python 04_langchain_langgraph/01_prompt_chaining/Notebooks/01_prompt_chaining_langgraph.py
	$(UV) run python 04_langchain_langgraph/02_parallelization/Notebooks/01_parallelization_langgraph.py
	$(UV) run python 04_langchain_langgraph/03_orchestrator_worker/Notebooks/01_orchestrator_worker_langgraph.py
	$(UV) run python 04_langchain_langgraph/04_evaluator_optimizer/Notebooks/01_evaluator_optimizer_langgraph.py
	$(UV) run python 04_langchain_langgraph/05_routing/Notebooks/01_routing_langgraph.py
	$(UV) run python 04_langchain_langgraph/06_agent_feedback/Notebooks/01_agent_feedback_langgraph.py

run-notebooks-langgraph: check-uv
	@echo " Executing Class 04 notebooks..."
	$(UV) run python 04_langchain_langgraph/tools/execute_notebooks.py

verify-notebooks-langgraph: run-notebooks-langgraph

test-se: check-uv
	$(UV) run pytest 01-introduction/python_software_engineering/tests -q

test-ai: check-uv
	$(UV) run pytest 01-introduction/ai_engineering/tests -v

test-ai-cov: check-uv
	$(UV) run pytest 01-introduction/ai_engineering/tests --cov=01-introduction/ai_engineering --cov-report=html

test-project: check-uv
	$(UV) run pytest 05_project/tests -q

test-all: check-uv
	$(UV) run pytest -v

lint: check-uv
	$(UV) run ruff check .

format: check-uv
	$(UV) run ruff format .

check:
	$(PYTHON) -m compileall 01-introduction 05_project/src

run-project: check-uv
	PYTHONPATH=05_project/src $(UV) run python -m multi_agent_system.main --query "$(QUERY)"

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
