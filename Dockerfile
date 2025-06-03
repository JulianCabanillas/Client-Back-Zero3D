FROM python:3.11-slim AS build

ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential slic3r libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=appBackClient.settings.staging

COPY wait-for.sh entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for.sh /usr/local/bin/entrypoint.sh

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos solo runtime deps (Postgres client y Slic3r)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev \
        netcat-openbsd\
        slic3r   \
    && rm -rf /var/lib/apt/lists/*

# Copiamos dependencias Python instaladas desde el build
COPY --from=build /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=build /usr/local/bin/ /usr/local/bin/

# Copiamos el código y el staticfiles (generado en build)
COPY --from=build /app /app

# Exponemos el puerto
EXPOSE 8000
# Entry point (espera DB, migraciones, etc.) y arranque Gunicorn
ENTRYPOINT ["./entrypoint.sh"]
