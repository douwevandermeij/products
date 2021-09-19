FROM tiangolo/uvicorn-gunicorn:python3.8-slim

RUN apt-get clean \
    && apt-get -y update \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential \
    && pip install pip --upgrade \
    && pip install pipenv \
    && rm -rf /var/lib/apt/lists/*

COPY ./Pipfile* /tmp/
RUN cd /tmp && pipenv install --system

COPY ./app /app/app
