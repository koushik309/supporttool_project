# Dockerfile
FROM python:3.10

WORKDIR /app

COPY . /app
COPY certs/ /app/certs/

ENV PYTHONPATH=/app


RUN pip install --no-cache-dir -r requirements.txt

CMD ["pytest"]
