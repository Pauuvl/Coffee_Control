from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def solo_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or (request.user.rol != "admin" and not request.user.is_superuser):
            messages.warning(request, "No tienes permisos de administrador para acceder a esta sección.")
            return redirect("no_autorizado")
        return view_func(request, *args, **kwargs)
    return wrapper

def solo_mesero(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.rol != "waiter":
            messages.warning(request, "No tienes permisos de mesero para acceder a esta sección.")
            return redirect("no_autorizado")
        return view_func(request, *args, **kwargs)
    return wrapper

def solo_superusuario(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.warning(request, "No tienes permisos de superusuario para acceder a esta sección.")
            return redirect("no_autorizado")
        return view_func(request, *args, **kwargs)
    return wrapper