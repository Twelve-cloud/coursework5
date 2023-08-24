# 1 layer
FROM python:3.10-alpine3.15

LABEL author="kana.suzucki@gmail.com"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2 layer
RUN apk update && apk add bash postgresql-dev gcc g++ python3-dev musl-dev && pip install poetry

WORKDIR /code
# 3 layer
COPY pyproject.toml poetry.toml /code
# 4 layer
RUN poetry config cache-dir /code/.poetry-cache && poetry install
# 5 layer
COPY . /code

# To use docker cache we copy all files in the end of Dockerfile.
# Otherwise if we change "COPY pyproject.toml poetry.toml /code" to "COPY . /code"
# docker will execute "RUN poetry config cache-dir /code/.poetry-cache && poetry install"
# everytime when we add new files to out directory.

# 6 layer
RUN chmod +x django-entrypoint.sh && chmod +x celery-entrypoint.sh && chmod +x celerybeat-entrypoint.sh && chmod +x migrations-entrypoint.sh
EXPOSE 8000
