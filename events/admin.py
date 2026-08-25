from django.contrib import admin
from .models import Evento
# Register your models here.

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'id_creador',
        'f_inicio',
        'f_fin',
        'estado',
        'created_at',
    )

    list_filter=(
        'estado',
        'f_inicio',
        'f_fin',
    )

    search_fields = (
        'titulo',
        'descripcion'
    )