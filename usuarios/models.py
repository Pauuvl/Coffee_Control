from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class ManejoUsuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('waiter', 'Mesero'),
    )
    rol = models.CharField(
        max_length=10,
        choices=ROLES,
        default='waiter'
    )
    

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
    
    # Permisos para Django Admin
    def has_perm(self, perm, obj=None):
        "¿Tiene permiso específico?"
        if self.rol == 'admin' or self.is_superuser:
            return True
        return super().has_perm(perm, obj)
    
    def has_module_perms(self, app_label):
        "¿Tiene permisos para ver el módulo en admin?"
        if self.rol == 'admin' or self.is_superuser:
            return True
        return super().has_module_perms(app_label)