from django.contrib import admin
from .models import Orden, ItemOrden

class ItemOrdenInline(admin.TabularInline): 
    model = ItemOrden
    extra = 0
    readonly_fields = ['producto', 'cantidad', 'precio', 'subtotal']
    
    def subtotal(self, obj):
        return f"${obj.cantidad * obj.precio}"
    subtotal.short_description = 'Subtotal'

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin): #Lo que se ve en el django admin
    list_display = ['id', 'mesero', 'tipo_pedido', 'estado', 'total', 'creado']
    list_filter = ['estado', 'tipo_pedido', 'creado', 'mesero']
    search_fields = ['id', 'mesero__username', 'nombre_cliente']
    readonly_fields = ['creado', 'actualizado']
    inlines = [ItemOrdenInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('mesero')

@admin.register(ItemOrden)
class ItemOrdenAdmin(admin.ModelAdmin):
    list_display = ['orden', 'producto', 'cantidad', 'precio', 'subtotal']
    list_filter = ['orden__estado', 'orden__creado']
    
    def subtotal(self, obj):
        return f"${obj.cantidad * obj.precio}"
    subtotal.short_description = 'Subtotal'