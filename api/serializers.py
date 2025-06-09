from rest_framework import serializers # type: ignore
from .models import Client, Order

# Estos serializadores nos ayudarana en la traduccion de los datos con la 
# base de datos mediante conversiones a JSON y viceversa.

# Serializador para los datos del cliente:
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_id','username', 'password', 'direction', 'email', 'date_register']
        # Nos aseguramos de que la contraseña solo se envie, nunca se 
        # mande a una peticion de usuario (Seguridad):
        extra_kwargs = {             
            'password': {'write_only': True}
        }

# Serializador para los datos del pedido:
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Order
        fields = ["order_id", "client", "technical",
                  "total_euros", "date_register", "stl_file", "material", "velocity", "color"]
        # Aqui tenemos las columnas que daremos valor una vez instaciados, utilizamos read_only_field
        # para que no gerenere fallos en el inicio (no sive estos datos en JSON) y darle valor 
        # a posterior en la vista:
        read_only_fields = ["order_id", "client", "technical", "date_register"]