FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH="/app/src"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --upgrade pip && pip install uv && uv pip install --system -e .

COPY src/ ./src/
COPY 00_datos/ ./00_datos/

EXPOSE 8006

CMD ["uvicorn", "cinematic_intelligence.api.main:app", "--host", "0.0.0.0", "--port", "8006"]
