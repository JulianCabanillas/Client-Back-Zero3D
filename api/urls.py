from django.urls import path # type: ignore
from . import views

# Aqui derivamos las peticiones entrantes a la API a su vista correspondiente:
urlpatterns = [
    path('register/', views.register_client, name='register_client'),
    path('clients/', views.get_clients, name='get_clients'),
    path('clients/<int:pk>/', views.get_client_by_id, name='get_client_by_id'),
    path('login/', views.login_client, name='login_client'),
    path('calculate/', views.calculate_budget, name='calculate_budget'),
]