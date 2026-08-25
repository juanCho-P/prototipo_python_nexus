from django.contrib import admin
from .models import Reporte
from .services import validar_reporte, invalidar_reporte


@admin.action(description='Validar reportes seleccionados (Aplicar Strike)')
def action_validar_reporte(modeladmin, request, queryset):
    for reporte in queryset:
        validar_reporte(reporte)

@admin.action(description='Invalidar reportes seleccionados')
def action_invalidar_reporte(modeladmin, request, queryset):
    for reporte in queryset:
        invalidar_reporte(reporte)


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'motivo',
        'estado',
        'id_usuario',
        'contenido_reportado',
        'created_at',
    )
    
    list_filter = (
        'estado',
        'motivo',
        'content_type',
    )
    
    search_fields = (
        'id_usuario__username',
        'comentario_adicional',
    )
    
    readonly_fields = (
        'created_at',
        'content_type',
        'object_id',
        'contenido_reportado',
    )
    
    actions = [
        action_validar_reporte,
        action_invalidar_reporte,
    ]