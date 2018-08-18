FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN groupadd -r django \
    && useradd -r -g django django
RUN pip install pipenv

# Install here so packages can be cached ahead of the app itself.
COPY Pipfile Pipfile.lock /
RUN pipenv install --dev --deploy --system --ignore-pipfile

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
