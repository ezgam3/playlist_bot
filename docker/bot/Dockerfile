FROM python:3.10.7-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/ezgame

RUN adduser --disabled-password --force-badname --gecos "" ezgame 
RUN usermod -a -G ezgame ezgame

ENV PROJECT_HOME=/home/ezgame/playlist_bot
RUN mkdir -p ${PROJECT_HOME}
WORKDIR ${PROJECT_HOME}

COPY ./docker/ ./docker/
COPY ./app/ ./app/
COPY ./alembic ./alembic
COPY ./poetry.lock .
COPY ./pyproject.toml .
COPY ./Makefile .
COPY ./alembic.ini .

RUN chmod +x ${PROJECT_HOME}/docker/bot/entrypoint.sh

RUN apt update
RUN apt install make
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir poetry
RUN python -m poetry config virtualenvs.create false
RUN python -m poetry install --no-dev --no-root

RUN chown -R ezgame:ezgame ${PROJECT_HOME}

USER ezgame

ENTRYPOINT ["/bin/sh", "/home/ezgame/playlist_bot/docker/bot/entrypoint.sh"]