from django.shortcuts import render # type: ignore
from django.contrib.auth import authenticate # type: ignore
from rest_framework.decorators import api_view, parser_classes, permission_classes # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken, TokenError # type: ignore
from rest_framework.parsers import MultiPartParser, FormParser # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from .models import Client
from .serializers import ClientSerializer, OrderSerializer
from .utils import calculator
from datetime import timedelta
from django.conf import settings # type: ignore
from .models import Order


# Vista para procesar la solicutud de login:
@csrf_exempt  # ---------------------> Solo desarrollo, evitamos err de CSRF
@api_view(['POST'])
def login_client(request):
    print("Datos recibidos:", request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    
    try:
        client = Client.objects.get(username=username, password=password)
    except Client.DoesNotExist:
        return Response({"error": "Credenciales incorrectas"}, status=400)

    # 1) Creamos refresh/access
    refresh = RefreshToken.for_user(client)
    refresh['username'] = client.username

    access  = refresh.access_token
    access['username'] = client.username


    # 2) Respondemos: access → JSON / refresh → cookie
    resp = Response({"access": str(access)}, status=200)

    set_refresh_cookie(resp, str(refresh))
    return resp

@api_view(['POST'])
def logout_client(request):
    resp = Response({"message": "Bye!"}, status=200)
    clear_refresh_cookie(resp)
    return resp

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])   # permite subir fichero
def create_order(request):
    """Registra un pedido con STL adjunto; el técnico queda null."""
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(client=request.user.client)   # cliente = user logeado
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@csrf_exempt
@api_view(['POST'])
def refresh_access_token(request):
    cookie = request.COOKIES.get("refresh_token")
    if cookie is None:
        return Response({"error": "Sin cookie"}, status=401)

    try:
        refresh = RefreshToken(cookie)
        access  = str(refresh.access_token)
        access['username'] = refresh['username']
        return Response({"access": access}, status=200)
    except TokenError:
        return Response({"error": "Refresh inválido"}, status=401)


# Vista para procesar la solicutud de registro:
@api_view(['POST'])
def register_client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_clients(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_client_by_id(request, pk):
    try:
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    except Client.DoesNotExist:
        return Response({"error": "Cliente no encontrado"}, status=404)

# Vista para la entrada a la calculadora:
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def calculate_budget(request):
    print("ENTRO EN CALCULATE_BUDGET")
    return calculator(request)


# --- 1.1 helper: poner cookie segura -------------------------
def set_refresh_cookie(resp, refresh_token: str):
    resp.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=int(timedelta(days=7).total_seconds()),
        httponly=True,
        secure=not settings.DEBUG,          # solo HTTPS fuera de DEBUG
        samesite="Strict",
    )

# --- 1.2 helper: borrar cookie (logout) ----------------------
def clear_refresh_cookie(resp):
    resp.delete_cookie("refresh_token")