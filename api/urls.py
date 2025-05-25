from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_client, name='register_client'),
    path('clients/', views.get_clients, name='get_clients'),
    path('clients/<int:pk>/', views.get_client_by_id, name='get_client_by_id'),
]