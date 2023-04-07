# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM python:3.10-slim as python-base

ENV SETUP_HOME="/opt/setup" \
    # python
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # others
    PATH="$SETUP_HOME/.venv/bin:$PATH"


# builder-base is used to build dependencies
FROM python-base as builder-base

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VERSION="1.4.1" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR $SETUP_HOME

RUN apt-get update && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
COPY poetry.lock pyproject.toml ./
RUN $POETRY_HOME/bin/poetry install --only main  # respects


FROM python-base as production

WORKDIR /code/

# Setup entrypoint
COPY misc/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT /docker-entrypoint.sh $0 $@

# Copy dependencies
COPY --from=builder-base $SETUP_HOME $SETUP_HOME

# Copy source
COPY manage.py ./manage.py
COPY migrations ./migrations
COPY jukebox ./jukebox

# Expose Network
EXPOSE 8000

# Run
CMD sh -c "python manage.py migrate && uvicorn jukebox.main:app"