from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum
from .models import Producto, Categoria, ItemCarrito
from .forms import FormularioProducto
from usuarios.decorators import solo_admin, solo_mesero
from decimal import Decimal

@login_required
def menu(request):
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria')
    query = request.GET.get('q', '')
    if request.user.rol == 'admin' or request.user.is_superuser:
        productos = Producto.objects.all() 
    else:
        productos = Producto.objects.filter(es_disponible=True)
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if query:
        productos = productos.filter(nombre__icontains=query)
    return render(request, 'menu.html', {
        'productos': productos,
        'categorias': categorias,
        'query': query
    })

@login_required
@login_required
def ver_carrito(request):
    items_carrito = ItemCarrito.objects.filter(usuario=request.user)
    
    # Calcular total de productos (suma de cantidades)
    total_productos = items_carrito.aggregate(total=Sum('cantidad'))['total'] or 0
    
    # Calcular totales
    total_carrito = sum(item.subtotal for item in items_carrito)
    impuestos = total_carrito * Decimal('0.10')
    total_general = total_carrito + impuestos
    
    context = {
        'items_carrito': items_carrito,
        'total_carrito': total_carrito,
        'impuestos': impuestos,
        'total_general': total_general,
        'total_productos': total_productos,
    }

    #Si la solicitud es AJAX, devolver solo el HTML parcial del carrito flotante
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'productos/carrito_contenido.html', context)
    
    #Si es una vista normal (URL /carrito/), se muestra la página completa
    return render(request, 'productos/carrito.html', context)

    
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if not producto.es_disponible:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Este producto no está disponible.'}, status=400)
        messages.error(request, "Este producto no está disponible.")
        return redirect('producto:menu')
    
    # Verificar si el item ya existe en el carrito
    item_carrito, created = ItemCarrito.objects.get_or_create(
        usuario=request.user,
        producto=producto,
        defaults={'cantidad': 1}
    )
    
    if not created:
        item_carrito.cantidad += 1
        item_carrito.save()
        mensaje = f"Se agregó otra unidad de {producto.nombre} al carrito."
    else:
        mensaje = f"Se agregó {producto.nombre} al carrito."
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        contador = ItemCarrito.objects.filter(usuario=request.user).aggregate(
            total=Sum('cantidad')
        )['total'] or 0
        
        return JsonResponse({
            'exito': True,
            'mensaje': mensaje,
            'contador_carrito': contador
        })
    
    messages.success(request, mensaje)
    return redirect('producto:menu')

@login_required
def actualizar_cantidad(request, item_id):
    item_carrito = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    action = request.POST.get('action')
    
    if action == 'increment':
        item_carrito.cantidad += 1
    elif action == 'decrement' and item_carrito.cantidad > 1:
        item_carrito.cantidad -= 1
    
    item_carrito.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        items_carrito = ItemCarrito.objects.filter(usuario=request.user)
        total_carrito = sum(item.subtotal for item in items_carrito)
        
        return JsonResponse({
            'success': True,
            'nueva_cantidad': item_carrito.cantidad,
            'nuevo_subtotal': float(item_carrito.subtotal),
            'nuevo_total': float(total_carrito)
        })
    
    return redirect('producto:ver_carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    item_carrito = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    producto_nombre = item_carrito.producto.nombre
    item_carrito.delete()
    
    messages.success(request, f"Se eliminó {producto_nombre} del carrito.")
    return redirect('producto:ver_carrito')

@login_required
def vaciar_carrito(request):
    ItemCarrito.objects.filter(usuario=request.user).delete()
    messages.success(request, "Se vació el carrito de compras.")
    return redirect('producto:ver_carrito')

@login_required
def obtener_contador_carrito(request):
    if request.user.is_authenticated:
        contador = ItemCarrito.objects.filter(usuario=request.user).aggregate(
            total=Sum('cantidad')
        )['total'] or 0
    else:
        contador = 0
    
    return JsonResponse({'contador': contador})

@login_required
def procesar_pedido(request):
    items_carrito = ItemCarrito.objects.filter(usuario=request.user)
    
    if not items_carrito:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('producto:menu')
    
    # Guardar items del carrito en la sesión
    carrito_session = []
    for item in items_carrito:
        carrito_session.append({
            'producto_id': item.producto.id,
            'cantidad': item.cantidad,
            'precio': float(item.producto.precio),
            'nombre': item.producto.nombre
        })
    
    request.session['carrito'] = carrito_session
    request.session.modified = True

    # Vaciar el carrito de la base de datos
    items_carrito.delete()
    
    # Redirigir al formulario de orden (GET)
    return redirect('ordenes:crear_orden')

#Solo para administradores
@solo_admin
def gestion_productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        formulario = FormularioProducto(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto agregado correctamente.")
            return redirect('producto:gestion_productos')
        else:
            messages.error(request, "Error al agregar el producto.")
    else:
        formulario = FormularioProducto()

    return render(request, 'productos/gestion_productos.html', {
        'productos': productos,
        'categorias': categorias,
        'formulario': formulario
    })

@solo_admin
def toggle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.es_disponible = not producto.es_disponible
    producto.save()
    estado = "disponible" if producto.es_disponible else "no disponible"
    messages.success(request, f"Producto marcado como {estado}.")
    referer = request.META.get('HTTP_REFERER', '')
    if 'menu' in referer:
        return redirect('producto:menu')
    else:
        return redirect('producto:gestion_productos')

@solo_admin
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto_nombre = producto.nombre
    producto.delete()
    messages.success(request, f"Producto '{producto_nombre}' eliminado correctamente.")
    referer = request.META.get('HTTP_REFERER', '')
    if 'menu' in referer:
        return redirect('producto:menu')
    else:
        return redirect('producto:gestion_productos')