from django.contrib import admin
from .models import Categoria, Producto, ItemCarrito

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'categoria', 'es_disponible']
    list_filter = ['categoria', 'es_disponible']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'es_disponible']

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'producto', 'cantidad', 'subtotal', 'creado']
    list_filter = ['usuario', 'creado']
    search_fields = ['usuario__username', 'producto__nombre']