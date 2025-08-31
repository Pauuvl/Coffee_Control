from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages 
from .models import Orden, ItemOrden
from productos.models import Producto
from .forms import FormularioDetallesOrden
from usuarios.decorators import solo_mesero 

@solo_mesero
def crear_orden(request):
    # Si es GET, mostrar el formulario
    if request.method == 'GET':
        # Calcular total del carrito (ahora es una lista)
        carrito = request.session.get('carrito', [])
        total_carrito = 0
        
        # Recorrer la lista en lugar del diccionario
        for item_data in carrito:
            total_carrito += item_data['precio'] * item_data['cantidad']
        
        return render(request, 'ordenes/crear_orden.html', {
            'total_carrito': total_carrito
        })
    
    # Si es POST, procesar la orden
    elif request.method == 'POST':
        tipo_pedido = request.POST.get('tipo_pedido', 'comer')
        numero_mesa = request.POST.get('numero_mesa')
        nombre_cliente = request.POST.get('nombre_cliente', '')
        comentarios = request.POST.get('comentarios', '')
        
        # Crear la orden
        orden = Orden.objects.create(
            mesero=request.user,
            tipo_pedido=tipo_pedido,
            numero_mesa=numero_mesa if tipo_pedido == 'comer' else None,
            nombre_cliente=nombre_cliente if tipo_pedido == 'llevar' else '',
            comentarios=comentarios,
            estado='pendiente',
            total=0
        )

        # Procesar items del carrito 
        carrito = request.session.get('carrito', [])
        total = 0

        for item_data in carrito:
            try:
                producto = Producto.objects.get(id=item_data['producto_id'])
                cantidad = item_data['cantidad']
                item_total = producto.precio * cantidad
                total += item_total

                ItemOrden.objects.create(
                    orden=orden,
                    producto=producto,
                    cantidad=cantidad,
                    precio=producto.precio
                )
            except Producto.DoesNotExist:
                continue

        # Actualizar total
        orden.total = total
        orden.save()

        # Limpiar carrito
        request.session['carrito'] = []
        request.session.modified = True
        
        messages.success(request, f"¡Orden #{orden.id} creada exitosamente!")
        return redirect('ordenes:detalle_orden', orden_id=orden.id)
    
@login_required #Administrador y mesero pueden ver la lista de ordenes
def listar_ordenes(request):
    ordenes = Orden.objects.all().order_by('-creado')
    if request.user.rol == 'waiter':
        ordenes = ordenes.filter(mesero=request.user) #El mesero solo ve sus propias ordenes

    return render(request, 'ordenes/lista_ordenes.html', {
        'ordenes': ordenes
    })

@login_required # 
def detalle_orden(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    if request.user.rol == 'waiter' and orden.mesero != request.user:
        messages.warning(request, "No tienes permisos para ver esta orden.")
        return redirect('ordenes:listar_ordenes') 

    return render(request, 'ordenes/detalle_orden.html', {'orden': orden})
