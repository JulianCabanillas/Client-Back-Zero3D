from rest_framework import serializers # type: ignore
from .models import Client, Order

# Serializador para los datos del cliente:
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_id','username', 'password', 'direction', 'email', 'date_register']
        extra_kwargs = {             
            'password': {'write_only': True}
        }

# Serializador para los datos del pedido:
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Order
        fields = ["order_id", "client", "technical",
                  "total_euros", "date_register", "stl_file"]
        read_only_fields = ["order_id", "technical", "date_register"]