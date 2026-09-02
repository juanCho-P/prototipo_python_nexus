from django.contrib import admin
from .models import Foro, Comentario

@admin.register(Foro)
class ForoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'descripcion', 'estado', 'created_at', 'imagen')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('estado', 'created_at', 'categoria')

   
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_foro', 'id_usuario', 'activo', 'created_at', 'has_image','contenido')
    search_fields = ('respuesta', 'id_usuario__username')
    list_filter = ('activo', 'created_at')

    @admin.display(boolean=True, description='¿Imagen?')
    def has_image(self, obj):
        return bool(obj.imagen)