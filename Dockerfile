FROM python:3.10-slim as base

FROM base as requirements
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM base as deployment
WORKDIR /code
EXPOSE 80
COPY --from=requirements /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./pubspec.yaml /code/
COPY ./pxm /code/pxm
CMD ["gunicorn", "-c", "./pxm/gunicorn.conf.py"]
