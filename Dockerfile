FROM python:3.11-slim

WORKDIR /app

# Utilizamos slic3r classic, version estable:
RUN apt-get update && apt-get install -y --no-install-recommends slic3r curl netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Establecemos el PATH para que este disponible a la llamada:
ENV SLIC3R_PATH=/usr/bin/slic3r

# PRESETS:
# skinnydip_fast.ini
# RUN mkdir -p slicer_profiles && \
#     curl -sSL \
#       https://raw.githubusercontent.com/supermerill/SuperSlicer/version_2.3.0/profiles/FDMS/skinnydip_fast.ini \
#       -o slicer_profiles/skinnydip_fast.ini

# Instalamos los requerimientos de entorno:
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ejecutamos el script para la espera de la BD:
COPY wait-for.sh entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for.sh /usr/local/bin/entrypoint.sh

# Entramos por script personalizado:
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

