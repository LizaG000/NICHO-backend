FROM python:3.11-slim AS backend

WORKDIR /app

COPY user_microservice/pyproject.toml user_microservice/poetry.lock* user_microservice/alembic.ini /app/

COPY deploy/configs /app/deploy/configs 

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY user_microservice/src /app/src

CMD ["uvicorn", "src.main.web:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

