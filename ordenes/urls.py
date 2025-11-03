from django.urls import path
from . import views

app_name = 'ordenes'  

urlpatterns = [
    path('crear-orden/', views.crear_orden, name='crear_orden'),
    path('lista-ordenes/', views.listar_ordenes, name='listar_ordenes'),
    path('detalle-orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('actualizar-estado/<int:orden_id>/<str:nuevo_estado>/', views.actualizar_estado_orden, name='actualizar_estado_orden'),
]