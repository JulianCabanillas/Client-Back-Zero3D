from django.urls import path, include

# Enlace principal por donde entra toda conexion a esta API y deriva:
urlpatterns = [
    path('api/', include('api.urls')) 
]
