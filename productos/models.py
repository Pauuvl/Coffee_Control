from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    imagen = models.ImageField(upload_to='categories/', blank=True, verbose_name="Imagen")

    def __str__(self):
        return self.nombre
        
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Producto(models.Model): 
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    precio = models.DecimalField(  
        max_digits=10,
        decimal_places=2, 
        verbose_name="Precio"
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE,  
        verbose_name="Categoría"
    )
    imagen = models.ImageField(
        upload_to='products/', 
        blank=True, 
        verbose_name="Imagen"
    )
    es_disponible = models.BooleanField(default=True, verbose_name="¿Disponible?")
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    actualizado = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    def __str__(self): 
        return f"{self.nombre} - ${self.precio}"  
    
    class Meta: 
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class ItemCarrito(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Usa el modelo personalizado
        on_delete=models.CASCADE,
        verbose_name="Usuario"
    )
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    cantidad = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Cantidad"
    )
    creado = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de creación"
    )
    actualizado = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última actualización"
    )
    
    class Meta:
        verbose_name = "Item del Carrito"
        verbose_name_plural = "Items del Carrito"
        unique_together = ['usuario', 'producto']
    
    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} - {self.usuario.username}"