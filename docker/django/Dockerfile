#!/bin/sh
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


# ---- system dependencies ----
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    librdkafka-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# 🚨 ENTRYPOINT MUST BE OUTSIDE /app (Codespaces noexec fix)
COPY docker/django/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
