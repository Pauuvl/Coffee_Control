from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import FormularioRegistro
from .models import ManejoUsuario
from .decorators import solo_admin

# Vista de registro SOLO para administradores
@solo_admin
def registro_mesero(request):
    if request.method == "POST":
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            usuario.rol = 'waiter'  # Siempre crea meseros
            usuario.is_staff = False  # Meseros no acceden al admin
            usuario.is_active = True  # Usuarios activos por defecto
            usuario.save()
            
            messages.success(request, f'Mesero {usuario.username} creado exitosamente!')
            return redirect('usuarios:lista_meseros')
    else:
        formulario = FormularioRegistro()

    return render(request, "usuarios/registro_mesero.html", {"formulario": formulario})

# Lista de meseros para administradores
@solo_admin
def lista_meseros(request):
    meseros = ManejoUsuario.objects.filter(rol='waiter').exclude(is_superuser=True)
    total_meseros = meseros.count()
    activos = meseros.filter(is_active=True).count()
    inactivos = total_meseros - activos
    
    context = {
        'meseros': meseros,
        'total_meseros': total_meseros,
        'activos': activos,
        'inactivos': inactivos
    }
    return render(request, "usuarios/lista_meseros.html", context)

# Vista de login normal
def login_view(request):
    if request.user.is_authenticated:
        return redirect('redireccionar')
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Bienvenido {user.username}!")
                return redirect('redireccionar')
            else:
                messages.error(request, "Cuenta desactivada. Contacta al administrador.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente')
    return redirect('inicio')