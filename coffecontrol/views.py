from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from usuarios.models import ManejoUsuario
from productos.models import Producto
from ordenes.models import Orden
from django.utils import timezone
from django.urls import reverse

def inicio(request):
    context = {}
    if request.user.is_authenticated and request.user.rol == "admin":
        context['meseros_count'] = ManejoUsuario.objects.filter(rol='waiter').count()
        context['productos_count'] = Producto.objects.count()
        hoy = timezone.now().date()
        context['ordenes_hoy_count'] = Orden.objects.filter(
            creado__date=hoy  
        ).count()
    
    return render(request, 'menu.html', context)

def no_autorizado(request):
    return render(request, 'no_autorizado.html')


def redireccionar(request):
    if request.user.is_superuser or request.user.rol == 'admin':
        return redirect(reverse('admin:index'))  # Admins van al Django Admin
    elif request.user.rol == 'waiter':
        return redirect('producto:menu')  #Meseros van al menú
    else:
        return redirect('home')  # Otros (no autenticados) van a inicio


def home(request):
    return render(request, 'inicio.html')