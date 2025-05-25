from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Client
from .serializers import ClientSerializer

@csrf_exempt  # Solo para desarrollo (evita errores de CSRF)
@api_view(['POST'])
def login_client(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Busca el cliente por username y contraseña
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