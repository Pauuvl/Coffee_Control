from django.urls import path
from . import views

app_name = 'producto'  

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('actualizar-cantidad/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('eliminar-del-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('procesar-pedido/', views.procesar_pedido, name='procesar_pedido'),
    path('obtener-contador-carrito/', views.obtener_contador_carrito, name='obtener_contador_carrito'),
    path('gestion-productos/', views.gestion_productos, name='gestion_productos'),
    path('toggle-producto/<int:producto_id>/', views.toggle_producto, name='toggle_producto'),
    path('eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]