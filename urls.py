# coffecontrol/urls.py (el archivo principal del proyecto)
from django.contrib import admin
from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Importamos las vistas de la app principal

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/registro/', views.registro, name='registro'),
    path('menu/', views.menu, name='menu'),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('crear-orden/', views.crear_orden, name='crear_orden'),
    path('ordenes/', views.listar_ordenes, name='listar_ordenes'),
    path('obtener-contador-carrito/', views.obtener_contador_carrito, name='obtener_contador_carrito'),
    
    # URLs para administradores
    path('admin/gestion-productos/', views.gestion_productos, name='gestion_productos'),
    path('admin/toggle-producto/<int:producto_id>/', views.toggle_producto, name='toggle_producto'),
    path('admin/eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]

# Para servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)