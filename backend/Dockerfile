FROM python:3.10

WORKDIR /app

#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src/main.py main.py
COPY src/config.py config.py
COPY __init__.py __init__.py

ENTRYPOINT ["uvicorn", "src.main:app", "--reload"]