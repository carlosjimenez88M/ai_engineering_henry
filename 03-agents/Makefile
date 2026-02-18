UV ?= uv
PYTHON ?= python3
VENV ?= .venv
VENV_PY ?= $(VENV)/bin/python
DATASET ?= LLMops/data/tickets_eval.jsonl
OUTPUT_DIR ?= LLMops/outputs

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
	@set -a; [ -f .env ] && . ./.env || true; set +a; \
	$(VENV_PY) -c 'from dotenv import load_dotenv; import os,sys; load_dotenv(); k=os.getenv("OPENAI_API_KEY"); print("OPENAI_API_KEY:", "OK" if k else "MISSING", f"(len={len(k) if k else 0})"); sys.exit(0 if k else 1)'
	@nslookup api.openai.com >/dev/null
	@set -a; [ -f .env ] && . ./.env || true; set +a; \
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
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook intro/01-que-es-un-agente.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook intro/02-workflows-vs-agentes.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook intro/03-costo-latencia-alucinacion.ipynb

notebooks-langchain:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook langchain/01-tool-calling.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook langchain/02-routing-condicional.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook langchain/03-validacion-salida.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook langchain/04-rag-agentico.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook langchain/05-flujo-agentico-completo.ipynb

notebooks-multi:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook multi-agent/01-orquestador-workers.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook multi-agent/02-handoffs.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook multi-agent/03-resolucion-conflictos.ipynb

notebooks-prod:
	@test -x $(VENV_PY) || $(MAKE) sync
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook production/01-timeouts-retries.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook production/02-fallback-guardrails.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook production/03-presupuesto-costos.ipynb
	$(VENV_PY) -m jupyter nbconvert --execute --to notebook production/04-alertas-calidad.ipynb

notebooks-all: notebooks-intro notebooks-langchain notebooks-multi notebooks-prod
