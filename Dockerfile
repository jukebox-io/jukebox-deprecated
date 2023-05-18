FROM python:3.11-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN python3 -m venv /pyenv

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT /docker-entrypoint.sh $0 $@

WORKDIR /opt


FROM python-base as requirements

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.4.2

RUN python3 -m pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./
RUN . /pyenv/bin/activate && poetry install --no-interaction --no-root --only main


FROM python-base as production

COPY --from=requirements /pyenv /pyenv
COPY jukebox ./jukebox

CMD ["uvicorn", "jukebox.main:app"]