from rest_framework import serializers # type: ignore
from .models import Client, Order

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_id','username', 'password', 'direction', 'email', 'date_register']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'client', 'technical', 'total_euros', 'date_register']