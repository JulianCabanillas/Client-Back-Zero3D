from django.shortcuts import render # type: ignore
from django.contrib.auth import authenticate # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from .models import Client
from .serializers import ClientSerializer

@csrf_exempt  # ---------------------> Solo desarrollo, evitamos err de CSRF
@api_view(['POST'])
def login_client(request):
    print("Datos recibidos:", request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        client = Client.objects.get(username=username, password=password)
        return Response({
            "message": "Login exitoso",
            "client_id": client.client_id,
            "username": client.username
        }, status=200)
    except Client.DoesNotExist:
        return Response({"error": "Credenciales incorrectas"}, status=400)

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