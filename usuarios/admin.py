from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from .models import ManejoUsuario

@admin.register(ManejoUsuario)
class ManejoUsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Rol Coffee Control', {
            'fields': ('rol',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('rol',)
        }),
    )
    
    # Solo superusuarios y admins pueden editar usuarios
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.rol == 'admin'
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.rol == 'admin'
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.rol == 'admin'
    
    # Limitar lo que los admins pueden ver/hacer
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superuser ve todo
        elif request.user.rol == 'admin':
            # Admin ve todos los usuarios excepto superusers
            return qs.exclude(is_superuser=True)
        return qs.none()
    
    # Prevenir que admins se hagan superusers o editen superusers
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            # Remover campos de superuser para admins normales
            if 'is_superuser' in form.base_fields:
                form.base_fields['is_superuser'].disabled = True
            if 'user_permissions' in form.base_fields:
                form.base_fields['user_permissions'].disabled = True
            if 'groups' in form.base_fields:
                form.base_fields['groups'].disabled = True
        return form
    
    # Acciones personalizadas
    actions = ['hacer_administradores', 'hacer_meseros', 'activar_usuarios', 'desactivar_usuarios']
    
    def hacer_administradores(self, request, queryset):
        if not request.user.is_superuser:
            # Admins solo pueden crear otros admins si son superusers
            messages.error(request, "Solo superusuarios pueden crear administradores")
            return
        
        count = queryset.update(rol='admin', is_staff=True)
        self.message_user(request, f"{count} usuarios convertidos en Administradores")
    hacer_administradores.short_description = "Convertir seleccionados en Administradores"
    
    def hacer_meseros(self, request, queryset):
        count = queryset.update(rol='waiter', is_staff=False)
        self.message_user(request, f"{count} usuarios convertidos en Meseros")
    hacer_meseros.short_description = "Convertir seleccionados en Meseros"
    
    def activar_usuarios(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} usuarios activados")
    activar_usuarios.short_description = "Activar usuarios seleccionados"
    
    def desactivar_usuarios(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} usuarios desactivados")
    desactivar_usuarios.short_description = "Desactivar usuarios seleccionados"