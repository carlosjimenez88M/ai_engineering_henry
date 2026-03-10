FROM python:3.13-slim
WORKDIR /src
ENV PYTHONPATH="/src"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependencias de compilación mínimas (gcc para algunas libs C)
RUN apt-get update \
    && apt-get -y install gcc g++ \
    && apt-get clean

COPY ./requirements.txt /src/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /src/requirements.txt

COPY ./TodoApp /src/TodoApp
COPY ./tests /src/tests

RUN ls /src
RUN ls /src/TodoApp/

CMD ["uvicorn", "TodoApp.main:app", "--host", "0.0.0.0", "--port", "8007"]
