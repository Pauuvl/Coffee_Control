from django import forms
from .models import Producto, Categoria

class FormularioProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'imagen', 'es_disponible']
        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción',
            'precio': 'Precio ($)',
            'categoria': 'Categoría',
            'imagen': 'Imagen del producto',
            'es_disponible': '¿Disponible?'
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe el producto...'}),
            'precio': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

class FormularioCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'imagen']
        labels = {
            'nombre': 'Nombre de la categoría',
            'descripcion': 'Descripción',
            'imagen': 'Imagen de la categoría'
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe la categoría...'}),
        }