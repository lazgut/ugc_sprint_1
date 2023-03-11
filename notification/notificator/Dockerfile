FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src src
COPY app.py app.py

ENTRYPOINT [ "flask", "run","--host","0.0.0.0","--port","5000"]
# TODO Use uwsgi.