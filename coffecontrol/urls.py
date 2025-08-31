from django.contrib import admin
from . import views # main views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('usuarios/', include('usuarios.urls')),
    path('productos/', include('productos.urls')),
    path('ordenes/', include('ordenes.urls')),
    path('no-autorizado/', views.no_autorizado, name='no_autorizado'), 
    path('redireccionar/', views.redireccionar, name='redireccionar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)