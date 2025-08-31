from django.urls import path
from . import views

app_name = 'ordenes'  

urlpatterns = [
    path('crear-orden/', views.crear_orden, name='crear_orden'),
    path('lista-ordenes/', views.listar_ordenes, name='listar_ordenes'),
    path('detalle-orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
]