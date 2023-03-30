FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install pip -U \
    && pip install --no-cache-dir -r requirements.txt

COPY src .

CMD ["python", "main.py"]
# ENTRYPOINT ["gunicorn", "main:app", "bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]