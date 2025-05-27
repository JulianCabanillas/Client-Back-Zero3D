FROM python:3.11-slim
RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Copiar el script wait-for y entrypoint
COPY wait-for.sh /wait-for.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /wait-for.sh /entrypoint.sh
# Ejecutamos entrypoint como punto de entrada
# Nos permite hacer el migrate y crear las tablas.
CMD ["/entrypoint.sh"]
