# syntax=docker/dockerfile:1
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt gunicorn==21.2.0

# app code
COPY . /app

# Azure MySQL CA (already added)
COPY azure-mysql-ca.pem /etc/ssl/certs/azure-mysql-ca.pem
ENV DB_SSL_CA=/etc/ssl/certs/azure-mysql-ca.pem

# make app files writable for non-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

ENV CONFIG_PATH=/app/config.json
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8080/ || exit 1

CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "8", "-b", "0.0.0.0:8080", "run:app"]
