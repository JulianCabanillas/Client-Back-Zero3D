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
@csrf_exempt  
@api_view(['POST'])
def login_client(request):
    # Utilizamnos el diccionario que nos transforma del JSON con  request.data:
    print("Datos recibidos:", request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    # Buscamos al usuario en la base de datos por el par user y pass, sino encontramos 
    # generamos un error 400:
    try:
        client = Client.objects.get(username=username, password=password)
    except Client.DoesNotExist:
        return Response({"error": "Credenciales incorrectas"}, status=400)

    # Creamos un token asociado al usuario cuando se logea de refresco y de acceso:
    refresh = RefreshToken.for_user(client)
    refresh['username'] = client.username

    access  = refresh.access_token
    access['username'] = client.username


    # Si se han podido generar sin problema, devolvemos el aceso en JSON y un 
    # estado 200, todo ok, llamando al metodo set_re.. para añadir la cookie:
    resp = Response({"access": str(access)}, status=200)
    set_refresh_cookie(resp, str(refresh))
    return resp

# Vista para la peticion de cerrar sesion del usuario, mediante el metodo 
# clear_re.. limpiamos las cookies:
@api_view(['POST'])
def logout_client(request):
    resp = Response({"message": "Bye!"}, status=200)
    clear_refresh_cookie(resp)
    return resp


# Vista para procesar la solicitud de pedido, comprueba usuario logeado, y 
# lo agrega para mandarlop a la base de datos
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Utilizamos para verificar que tenemos user logeado.
@parser_classes([MultiPartParser, FormParser]) # Utilizamos para transformar el dataForm.  
def create_order(request):
    # Utilizamos el serializer para convertir los que nos viene del Front y si todo es 
    # valido creamos la orden y le añadimos el cliente que la esta realizando:
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        # Añadimos cliente:
        order = serializer.save(client=request.user)
        # Si todo correcto generamos rtepuesta con el JSON y el estado 201, pedido ok:
        return Response(OrderSerializer(order).data, status=201)
    # Sino generamos error 400:
    return Response(serializer.errors, status=400)

# Vista para el refresco y renuevo del acceso del usuario:
@csrf_exempt
@api_view(['POST'])
def refresh_access_token(request):
    # Buscaremos la Cookie correspondiente y si no la encontramos, arrojamos error 401:
    cookie = request.COOKIES.get("refresh_token")
    if cookie is None:
        return Response({"error": "Sin cookie"}, status=401)

    # Si la cookie fue encontrada validaremos y extraemos el token de nuevo 
    # y refrescaremos para el usuario concreto:
    try:
        refresh = RefreshToken(cookie)
        access  = str(refresh.access_token)
        access['username'] = refresh['username']
        return Response({"access": access}, status=200)
    # Si hay algun problema con el refresco, arrojamos error 401:
    except TokenError:
        return Response({"error": "Refresh inválido"}, status=401)


# Vista para procesar la solicutud de registro:
@api_view(['POST'])
def register_client(request):
    # Recuperamos los datos:
    serializer = ClientSerializer(data=request.data)
    # Si todo esta correcto pasa al guardado en bd, si todo correcto estado 201:
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    # En el caso de querer insertar un cliente cuyas claves unicas (user/email) 
    # se repiten, arrojara error 400 y se informara al usuario con un alert:
    return Response(serializer.errors, status=400)


# Vista para futuras actualizaciones, lista de todos los clientes:
@api_view(['GET'])
def get_clients(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)

# Vista para futuras actualizaciones, cliente por id:
@api_view(['GET'])
def get_client_by_id(request, pk):
    try:
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    except Client.DoesNotExist:
        return Response({"error": "Cliente no encontrado"}, status=404)


# Vista para la entrada a la calculadora, solo hago de entrada y mando la infrmacion
# al la clase calculator para que me devuelva una respuesta de los calculos:
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def calculate_budget(request):
    return calculator(request)


# Metodo AUXILIAR para refrescar la cookie:
def set_refresh_cookie(resp, refresh_token: str):
    resp.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=int(timedelta(days=7).total_seconds()),
        httponly=True,
        secure=not settings.DEBUG,          
        samesite="Strict",
    )

# Metodo AUXILIAR para borrar el refres_token (Cookie):
def clear_refresh_cookie(resp):
    resp.delete_cookie("refresh_token")