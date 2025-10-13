from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages 
from .models import Orden, ItemOrden
from productos.models import Producto
from .forms import FormularioDetallesOrden
from usuarios.decorators import solo_mesero 
from decimal import Decimal

@solo_mesero
def crear_orden(request):
    # Si es GET, mostrar el formulario
    if request.method == 'GET':
        # Calcular total del carrito
        carrito = request.session.get('carrito', [])
        subtotal = Decimal('0.00')
        
        for item_data in carrito:
            precio = Decimal(str(item_data['precio']))
            cantidad = Decimal(str(item_data['cantidad']))
            subtotal += precio * cantidad
        
        impuestos = subtotal * Decimal('0.10')
        total_general = subtotal + impuestos
        
        return render(request, 'ordenes/crear_orden.html', {
            'subtotal': subtotal,
            'impuestos': impuestos,
            'total_general': total_general
        })
    
    # Si es POST, procesar la orden
    elif request.method == 'POST':
        tipo_pedido = request.POST.get('tipo_pedido', 'comer')
        numero_mesa = request.POST.get('numero_mesa')
        nombre_cliente = request.POST.get('nombre_cliente', '')
        comentarios = request.POST.get('comentarios', '')
        metodo_pago = request.POST.get('metodo_pago', 'efectivo')
        
        # Calcular subtotal del carrito
        carrito = request.session.get('carrito', [])
        subtotal = Decimal('0.00')

        for item_data in carrito:
            try:
                # Convertir a Decimal para evitar problemas de tipo
                precio = Decimal(str(item_data['precio']))
                cantidad = Decimal(str(item_data['cantidad']))
                subtotal += precio * cantidad
            except (ValueError, TypeError):
                continue

        impuestos = subtotal * Decimal('0.10')
        total_general = subtotal + impuestos

        # Crear la orden
        orden = Orden.objects.create(
            mesero=request.user,
            tipo_pedido=tipo_pedido,
            metodo_pago=metodo_pago,
            numero_mesa=numero_mesa if tipo_pedido == 'comer' else None,
            nombre_cliente=nombre_cliente if tipo_pedido == 'llevar' else '',
            comentarios=comentarios,
            estado='pendiente',
            subtotal=subtotal,
            impuestos=impuestos,
            total=total_general
        )

        # Procesar items del carrito 
        for item_data in carrito:
            try:
                producto = Producto.objects.get(id=item_data['producto_id'])
                cantidad = item_data['cantidad']

                ItemOrden.objects.create(
                    orden=orden,
                    producto=producto,
                    cantidad=cantidad,
                    precio=producto.precio  # Esto ya es Decimal del modelo
                )
            except (Producto.DoesNotExist, KeyError):
                continue

        # Limpiar carrito
        request.session['carrito'] = []
        request.session.modified = True
        
        messages.success(request, f"¡Orden #{orden.id} creada exitosamente!")
        return redirect('ordenes:detalle_orden', orden_id=orden.id)
    
@login_required 
def listar_ordenes(request):
    if request.user.rol == 'admin' or request.user.is_superuser:
        ordenes = Orden.objects.all().order_by('-creado')
    else:
        ordenes = Orden.objects.filter(mesero=request.user).order_by('-creado')    
    
    # Filtrado por estado
    estado_filtro = request.GET.get('estado', 'todas')
    if estado_filtro != 'todas':
        ordenes = ordenes.filter(estado=estado_filtro)

    return render(request, 'ordenes/lista_ordenes.html', {
        'ordenes': ordenes,
        'estado_actual': estado_filtro
    })

@login_required
def detalle_orden(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)
    puede_ver = (
        (request.user.rol == 'waiter' and orden.mesero == request.user) or
        request.user.rol == 'admin' or
        request.user.is_superuser
    )
    if not puede_ver:
        messages.warning(request, "No tienes permisos para ver esta orden.")
        return redirect('ordenes:listar_ordenes') 

    return render(request, 'ordenes/detalle_orden.html', {'orden': orden})

@login_required
def actualizar_estado_orden(request, orden_id, nuevo_estado):
    orden = get_object_or_404(Orden, id=orden_id)

    if request.user.rol not in ['admin', 'waiter']:
        messages.error(request, "No tienes permisos para cambiar el estado de esta orden.")
        return redirect('ordenes:listar_ordenes')

    if nuevo_estado in [estado[0] for estado in Orden.ESTADOS]:
        orden.estado = nuevo_estado
        orden.save()
        messages.success(request, f"El estado de la orden #{orden.id} ha sido actualizado a '{orden.get_estado_display()}'.")
    else:
        messages.error(request, "Estado no válido.")

    return redirect('ordenes:listar_ordenes')