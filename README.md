# Client‑Back‑Zero3D

## ️🧩 Descripción

Es el servicio REST para la suite Suite-Zero3D, resuelve todos los endpoints necesarios para la logica deltras de PREACT.
Realizado en **Django** + **Django REST Framework**.
Uso de librerías como **CORS**

---

## 🚀 Puesta en marcha rápida

Revisar README del contenedor padre: https://github.com/JulianCabanillas/Suite-Zero3D.git

## 🔧 Variables de entorno principales

| Nombre              | Ejemplo       | Descripción          |
| ------------------- | ------------- | -------------------- |
| `DB_HOST`           | `localhost`   | Host de Postgres     |
| `DB_USER`           | `zero3d_user` | Usuario BD           |
| `DB_PASSWORD`       | `supersegura` | Contraseña           |
| `DJANGO_SECRET_KEY` | `changeme`    | Clave secreta Django |
| `DEBUG`             | `True`        | Mostrar trazas       |

---

## 📂 Estructura básica

```

Client-backZero3D/
├─ api/             # Carpeta con los archivos de la api necesarios.
├─ appBackClient/   # Carpeta con los archivos necesarios para comerzar como main
└─ slicer_profiles/ # Carpeta con los perfiles por defecto del slicer o personalizados

```

---

## 📚 Migraciones y datos de ejemplo

```bash
python manage.py migrate          # aplica migraciones
python manage.py loaddata seeds   # carga datos dummy 
```

---

## 🛠️ Comandos útiles

| Acción             | Comando                            |
| ------------------ | ---------------------------------- |
| Ejecutar tests     | `pytest`                           |
| Crear superusuario | `python manage.py createsuperuser` |

---

## 📑 Endpoints principales (resumen)

| Método | Endpoint                 | Descripción                      |
| ------ | ------------------------ | -------------------------------- |
| `POST` | `/api/login_client/`     | Autenticación y obtención de JWT |
| `POST` | `/api/register_client/`  | Registra y posterior hace login  |
| `POST` | `/api/register_order/`   | Registra pedido con el usuario   |
| `POST` | `/api/calculator/`       | Calcula precio de impresión 3D   |

---

## 🐳 Dockerfile

Si modificas requirements a la hora de crear nuevo desarrollo, reconstruye con:

```bash
docker compose build back
```

---

## 📝 Licencia

Este proyecto se distribuye bajo la licencia **GNU General Public License**. Consulta el archivo `LICENSE` para más información.
