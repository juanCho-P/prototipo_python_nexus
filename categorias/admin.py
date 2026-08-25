from django.contrib import admin
from .models import Categoria
# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  # Muestra el ID y el nombre de la categoría en la lista de administración
    search_fields = ('nombre',)  # Permite buscar categorías por nombre