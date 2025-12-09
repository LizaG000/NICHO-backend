FROM python:3.11-slim AS backend

WORKDIR /app

COPY order_microservice/pyproject.toml order_microservice/poetry.lock* user_microservice/alembic.ini /app/

COPY deploy/configs /app/deploy/configs 

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY order_microservice/src /app/src

CMD ["sh", "-c", "uvicorn src.main.web:app --host $USER_MICRO_HOST --port $USER_MICRO_PORT --reload"]

