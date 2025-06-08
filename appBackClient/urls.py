from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Enlace principal por donde entra toda conexion a esta API y deriva:
urlpatterns = [
    path('api/', include('api.urls')) 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
