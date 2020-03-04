FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN groupadd -r django \
    && useradd -r -g django django
RUN pip install poetry

# Install here so packages can be cached ahead of the app itself.
COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false \
  && poetry install --verbose --no-dev --no-interaction --no-ansi

COPY ./compose/django/gunicorn.sh ./compose/django/entrypoint.sh /
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

COPY . /app

RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
