from django import forms
from .models import Orden, ItemOrden

class FormularioDetallesOrden(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['tipo_pedido', 'numero_mesa', 'nombre_cliente', 'comentarios']
        labels = {
            'tipo_pedido': '¿El pedido es para:',
            'numero_mesa': 'Número de mesa',
            'nombre_cliente': 'Nombre del cliente',
            'comentarios': 'Comentarios adicionales',
        }
        widgets = {
            'tipo_pedido': forms.RadioSelect(),
            'numero_mesa': forms.NumberInput(attrs={'min': '1', 'max': '20', 'id': 'id_numero_mesa'}),
            'nombre_cliente': forms.TextInput(attrs={'id': 'id_nombre_cliente', 'placeholder': 'Ej: María García'}),
            'comentarios': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ej: Café sin azúcar, pan bien tostado...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['numero_mesa'].widget.attrs['style'] = 'display:none;'
        self.fields['nombre_cliente'].widget.attrs['style'] = 'display:none;'
        self.fields['tipo_pedido'].widget.choices = self.Meta.model.TIPO_PEDIDO

class FormularioItemOrden(forms.ModelForm):
    class Meta:
        model = ItemOrden
        fields = ['producto', 'cantidad', 'notas']
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'notas': 'Notas especiales'
        }
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': '1', 'max': '10'}),
            'notas': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ej: Sin hielo, bien dulce...'}),
        }