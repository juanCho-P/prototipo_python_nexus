from django.contrib import admin
from .models import Foro, Comentario

@admin.register(Foro)
class ForoAdmin(admin.ModelAdmin):
    list_display = ('id','titulo', 'descripcion', 'estado', 'created_at','imagen')
    search_fields = ('titulo', 'descripcion', 'categoria')
    list_filter = ('categoria', 'created_at')

    list_filter = ('estado', 'created_at', 'categoria')

    search_fields = ('titulo', 'descripcion')

   
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_foro', 'id_usuario', 'created_at', 'activo', 'created_at' , 'imagen')
    search_fields = ('respuesta', 'id_usuario')

    @admin.display(boolean=True, description='imagen?')
    def has_image(self, obj):
        return bool(obj.imagen)



