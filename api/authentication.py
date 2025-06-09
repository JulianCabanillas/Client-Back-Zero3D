from rest_framework_simplejwt.authentication import JWTAuthentication  # type: ignore
from rest_framework.exceptions import AuthenticationFailed  # type: ignore
from .models import Client

# Clase  creada con el proposito de heredar la clase JWTAuthentication y modificar 
# el comportamiento para nuestro caso concreto, vamos a recuperar los datos del 
# diccionaro validated_token para ver a que cliente le pertenece las peticiones:

class ClientJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # Compurbea que exista dicho usuario:
        client_id = validated_token.get("client_id")
        if client_id is None:
            # Si no tenemos la informacion en el token, error:
            raise AuthenticationFailed("Token sin client_id")
        try:
            # Si existe buscara el cliente en la base de datos cuya id cincida 
            # con la del token:
            return Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            # Si no existe el cliente, lanzamos error:
            raise AuthenticationFailed("Cliente no encontrado")