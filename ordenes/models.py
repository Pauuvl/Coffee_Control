from django.db import models
from usuarios.models import ManejoUsuario 
from productos.models import Producto 

class Orden(models.Model): 
    TIPO_PEDIDO = (
        ('comer', 'Para comer aquí'), 
        ('llevar', 'Para llevar'),
    )
    ESTADOS = ( 
        ('pendiente', 'Pendiente'),  
        ('preparando', 'En preparación'), 
        ('listo', 'Listo'), 
        ('entregado', 'Entregado'), 
        ('cancelado', 'Cancelado'),
    )
    
    mesero = models.ForeignKey(  
        ManejoUsuario, 
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'waiter'},  
        verbose_name="Mesero"
    )
    tipo_pedido = models.CharField(  
        max_length=10, 
        choices=TIPO_PEDIDO, 
        default='comer',  
        verbose_name="Tipo de pedido"
    )
    numero_mesa = models.IntegerField(
        verbose_name="Número de mesa", 
        null=True,  
        blank=True
    )
    nombre_cliente = models.CharField(
        max_length=100, 
        verbose_name="Nombre del cliente",
        blank=True
    )
    comentarios = models.TextField(
        blank=True, 
        verbose_name='Comentarios adicionales'
    )
    estado = models.CharField(  
        max_length=10, 
        choices=ESTADOS,  
        default='pendiente',  
        verbose_name="Estado"
    )
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")  
    actualizado = models.DateTimeField(auto_now=True, verbose_name="Última actualización")  
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name="Total"
    )

    def __str__(self):
        return f"Orden #{self.id} - {self.get_tipo_pedido_display()} - {self.get_estado_display()}"  

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"

class ItemOrden(models.Model):  
    orden = models.ForeignKey(  
        Orden, 
        related_name='items', 
        on_delete=models.CASCADE,
        verbose_name="Orden"
    )
    producto = models.ForeignKey(
        Producto,  
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    cantidad = models.IntegerField(default=1, verbose_name="Cantidad")
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Precio unitario"
    )
    notas = models.TextField(
        blank=True, 
        verbose_name="Notas"
    )  

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} - ${self.precio * self.cantidad}"

    class Meta: 
        verbose_name = "Item de orden"
        verbose_name_plural = "Items de orden"
