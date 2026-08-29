from django.contrib import admin
from .models import Usuario,Rol

# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):

    list_display = (
        'id_usuario',
        'username',
        'email',
        'nombres',
        'apellidos',
        'rol',
        'estado',
        'strikes',
        'email_verificado',
        'is_active',
        'created_at',
    )

    list_filter = (
        'rol',
        'estado',
        'email_verificado',
        'is_active'
    )

    search_fields = (
        'username',
        'email',
        'nombress',
        'apellidos'
    )

    list_editable = (
        'email_verificado',
        'is_active',
        'strikes'
        
)


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):

    list_display= (
        'id_rol',
    )

    

