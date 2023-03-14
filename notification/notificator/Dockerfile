FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

COPY run_uwsgi.sh run_uwsgi.sh
COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app.py app.py
COPY build build

ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]