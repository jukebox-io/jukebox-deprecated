# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM python:3.11-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN python3 -m venv /pyenv

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT /entrypoint.sh $0 $@

WORKDIR /opt


# Installing required dependencies
FROM python-base as setup

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.4.2

RUN python3 -m pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./
RUN . /pyenv/bin/activate && poetry install --no-interaction --no-root --only main


# 'production' stage uses the clean 'python-base' stage and copyies
# in only our runtime deps that were installed in the 'setup' stage
FROM python-base as production

COPY --from=setup /pyenv /pyenv
COPY jukebox ./jukebox

EXPOSE 8000
CMD ["uvicorn", "jukebox.main:app", "--host", "0.0.0.0", "--port", "8000"]
