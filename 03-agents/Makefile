UV ?= uv
PYTHON ?= python3
VENV ?= .venv
VENV_PY ?= $(VENV)/bin/python
DATASET ?= 05_llmops/00_data/tickets_eval.jsonl
OUTPUT_DIR ?= 05_llmops/outputs

.PHONY: install sync sync-pip lint format test doctor run-llmops run-llmops-nojudge \
        notebooks-intro notebooks-langchain notebooks-multi notebooks-prod notebooks-all

install: sync

sync:
	$(UV) sync --extra dev || $(MAKE) sync-pip

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

doctor:
	@test -x $(VENV_PY) || $(MAKE) sync
	@echo "== Doctor: entorno y conectividad OpenAI =="
	@set -a; if [ -f .env ]; then . ./.env; elif [ -f ../.env ]; then . ../.env; fi; set +a; \
	$(VENV_PY) -c 'from dotenv import load_dotenv; import os,sys; load_dotenv(); k=os.getenv("OPENAI_API_KEY"); print("OPENAI_API_KEY:", "OK" if k else "MISSING", f"(len={len(k) if k else 0})"); sys.exit(0 if k else 1)'
	@nslookup api.openai.com >/dev/null
	@set -a; if [ -f .env ]; then . ./.env; elif [ -f ../.env ]; then . ../.env; fi; set +a; \
	code=$$(curl -sS -o /tmp/openai_models_doctor.json -w "%{http_code}" https://api.openai.com/v1/models -H "Authorization: Bearer $$OPENAI_API_KEY"); \
	echo "OpenAI /v1/models HTTP $$code"; \
	test "$$code" = "200"
	@echo "Doctor OK: DNS y API accesibles."

run-llmops:
	@test -x $(VENV_PY) || $(MAKE) sync
	OPENAI_MODEL=gpt-5-mini $(VENV_PY) -m llmops.main --dataset $(DATASET) --output-dir $(OUTPUT_DIR) --judge

run-llmops-nojudge:
	@test -x $(VENV_PY) || $(MAKE) sync
	OPENAI_MODEL=gpt-5-mini $(VENV_PY) -m llmops.main --dataset $(DATASET) --output-dir $(OUTPUT_DIR) --no-judge

# --- Notebooks ---

notebooks-intro:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 01_intro/01_que_es_un_agente.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 01_intro/02_workflows_vs_agentes.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 01_intro/03_costo_latencia_alucinacion.ipynb

notebooks-langchain:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 02_langchain/01_tool_calling.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 02_langchain/02_routing_condicional.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 02_langchain/03_validacion_salida.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 02_langchain/04_rag_agentico.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 02_langchain/05_flujo_agentico_completo.ipynb

notebooks-multi:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 03_multi_agent/01_orquestador_workers.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 03_multi_agent/02_handoffs.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 03_multi_agent/03_resolucion_conflictos.ipynb

notebooks-prod:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 04_production/01_timeouts_retries.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 04_production/02_fallback_guardrails.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 04_production/03_presupuesto_costos.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook 04_production/04_alertas_calidad.ipynb

notebooks-all: notebooks-intro notebooks-langchain notebooks-multi notebooks-prod
