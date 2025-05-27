#!/bin/sh

# Ante cualquier fallo, esta linea evita que siga ejecutando:
set -e

# Antes de empezar validamos los argumentos que nos pasan:
if [ -z "$1" ]; then
  echo "Uso: $0 host:port comando..."
  exit 1
fi

# Para netcat debemos de separar el host del port:
HOST_PORT="$1"

# Elimina el primer argumento (HOST_PORT)
shift

# Utilizamos cut para separar la cadena HOST_PORT
HOST=$(echo "$HOST_PORT" | cut -d: -f1)
PORT=$(echo "$HOST_PORT" | cut -d: -f2)


# Comprobacion para el corte, verifica cadena:
if [ -z "$HOST" ] || [ -z "$PORT" ]; then
  echo "Error: formato incorrecto de host:port — se esperaba algo como db:5432"
  exit 1
fi

echo "Esperando que $HOST:$PORT esté disponible..."

# Bucle donde esperamos a que el puerto de la base de datos este disponible
# para continuar con el script, con until no para hasta que realiza la accion:
until nc -z "$HOST" "$PORT"; do
  echo "Esperando que $HOST:$PORT esté disponible..."
  sleep 1
done

echo "$HOST:$PORT está disponible. Ejecutando comando..."

# Verificamos que el comando que viene sea válido, sino sale y continua:
if [ $# -eq 0 ]; then
  echo "Error: no se pasó ningún comando a ejecutar"
  exit 1
fi

# Si todo a sido correcto ejecutmos los comandos restantes con "$@":
exec "$@"
