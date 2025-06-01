from decimal import Decimal, InvalidOperation
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.core.validators import FileExtensionValidator # type: ignore
from decimal import Decimal, InvalidOperation
from rest_framework import status  # type: ignore
from rest_framework.parsers import MultiPartParser, FormParser # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.decorators import parser_classes # type: ignore
import tempfile
import os
import os
import re
import subprocess
import tempfile
from pathlib import Path

_PRICE_METER = {"pla": 5.5, "abs": 8.8, "petg": 7.4}
_CURA_OFFSET_MATERIAL = 2
_CURA_OFFSET_TIME = 4.2

# Metodo para calcular el precio, separado por comodidad:
def _calculate_price(material_m, material_key, minutes):
    return (material_m * _PRICE_METER.get(material_key, 5.0)) + (minutes * 1.5)


# Metodo principal.
# Aqui recuperamos los datos que recibimos del front y tratamos los datos para el calculo:
@parser_classes([MultiPartParser, FormParser])
def calculator(request):
    stl_file = request.FILES.get("file")
    material = request.data.get("material")
    velocity = request.data.get("velocity")

    # Debemos de validar que llegan todos los parametros necesarios:
    if not all([stl_file, material, velocity]):
        return Response({"error": "Faltan parámetros"}, status=status.HTTP_400_BAD_REQUEST)

    # Intentamos hacer el casting de la velocidad:
    try:
        velocity = Decimal(velocity)
        # Si nos da menor que cero, invalidamos:
        if velocity <= 0:
            raise InvalidOperation
    except (InvalidOperation, TypeError):
        return Response(
            {"error": "La velocidad debe ser numérica"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Pasamos a crear un archivo temporal para el calculo:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp_file:
        for chunk in stl_file.chunks():
            tmp_file.write(chunk)
        tmp_file_path = tmp_file.name

    try:
            # Una vez todo correcto pasamos el archivo temporal a la funcion que procesara el archivo para el calculo:
        results = calculation(tmp_file_path, material, velocity) 

        return Response(
            {
                "time": results["time"],
                "material_required": results["material_required"],
                "total_price": results["total_price"],
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    finally:
        # Nos aseguramos de borrar el archivo temporal despues del calculo:
        os.unlink(tmp_file_path)


# Metodo que hara cortado del archivo y calculara el precio:
def calculation(file_path: str, material: str, velocity: int):

    slic3r = os.getenv("SLIC3R_PATH", "/usr/bin/slic3r")
    profile = Path.cwd() / "slicer_profiles" / "slic3r_default.ini"
    if not profile.is_file():
        raise FileNotFoundError(f"Perfil de Slic3r no encontrado: {profile}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".gcode") as tmp:
        gcode_path = tmp.name

        # Aqui preparamos la llamada al slicer
        cmd = [
            slic3r,
            "--output", gcode_path,
            "--gcode-comments",                # vuelca "filament used" y "print time"
            "--load", str(profile),
            str(file_path),
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"Error en Slic3r: {exc.stderr}") from exc

        # Esperamos a una salida y parseamos para el calculo:
        material_m, time_min = _gcode(gcode_path, velocity)
        
        # Comprobamos que esten los datos fuera de nulo:
        if material_m is None or time_min is None:
            with open(gcode_path, encoding="utf-8", errors="ignore") as fh:
                header = "".join(fh.readline() for _ in range(10))
            raise RuntimeError(
                "No se pudo extraer tiempo o material de Slic3r\n"
                f"(material={material_m}, tiempo={time_min}).\n"
                f"G-code header sample:\n{header}"
            )
        material_m = material_m * _CURA_OFFSET_MATERIAL
        time_min = time_min * _CURA_OFFSET_TIME

        # Si esta todo correcto mandamos a la funcion de calcular precio:
        total_price = _calculate_price(material_m, material.lower(), time_min)
        
        return {
            "time": time_min,
            "material_required": material_m,
            "total_price": total_price,
        }


# Metodo para parsear el gcode:
def _gcode(gcode_path, velocity):
    # Utilizamos la libreria de expresiones regulares para extraer la informacion:
    fil_pat  = re.compile(r'filament\s*used\s*[=:]\s*([\d.]+)\s*(mm|m)', re.I)
    time_pat = re.compile(
        r'estimated.*?print(?:ing)?\s*time.*?[=:]\s*'
        r'((?:\d+h)?\s*(?:\d+m)?\s*(?:\d+s)?)',
        re.I,
    )
    hrs_mins_pat = re.compile(r'(\d+)\s*h\s*(\d+)\s*m', re.I)
    mins_pat     = re.compile(r'([\d.]+)\s*min', re.I)

    material_m = time_min = None
    with open(gcode_path, encoding="utf-8", errors="ignore") as fh:
        for ln in fh:
            if (m := fil_pat.search(ln)):
                val, unit = float(m[1]), m[2].lower()
                material_m = val / 1000 if unit == "mm" else val
            if (m := time_pat.search(ln)):
                txt = m[1]
                h  = sum(float(t[:-1]) for t in txt.split() if t.endswith("h"))
                m_ = sum(float(t[:-1]) for t in txt.split() if t.endswith("m"))
                s  = sum(float(t[:-1]) for t in txt.split() if t.endswith("s"))
                time_min = h * 60 + m_ + s / 60

            elif time_min is None and (m := hrs_mins_pat.search(ln)):
                time_min = int(m[1]) * 60 + int(m[2])
            elif time_min is None and (m := mins_pat.search(ln)):
                time_min = float(m[1])

    # Si por algun caso no tenemos tiempo de impresion, lo calculamos 
    # por material necesario:
    if time_min is None and material_m is not None:
        v = max(int(velocity), 1)
        time_min = material_m * 1000 / (v * 60) * 1.15

    return material_m, time_min