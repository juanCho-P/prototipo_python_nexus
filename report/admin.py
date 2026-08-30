from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from .models import Reporte
from .services import validar_reporte, invalidar_reporte

@admin.action(description='Validar reporte y aplicar +1 Strike al infractor')
def aprobar_reportes_action(modeladmin, request, queryset):
    procesados = 0
    for reporte in queryset:
        if validar_reporte(reporte):
            procesados += 1
    modeladmin.message_user(
        request, 
        f"Se aprobaron {procesados} reportes exitosamente.", 
        messages.SUCCESS
    )

@admin.action(description='Rechazar reportes seleccionados')
def rechazar_reportes_action(modeladmin, request, queryset):
    procesados = 0
    for reporte in queryset:
        if invalidar_reporte(reporte):
            procesados += 1
    modeladmin.message_user(
        request, 
        f"Se rechazaron {procesados} reportes.", 
        messages.INFO
    )

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'reportador', 
        'reportado', 
        'content_type', 
        'ver_contenido',  # Columna personalizada para inspeccionar el texto
        'motivo', 
        'estado', 
        'created_at'
    )
    list_filter = ('estado', 'content_type', 'created_at')
    search_fields = ('reportador__username', 'reportado__username', 'motivo')
    actions = [aprobar_reportes_action, rechazar_reportes_action]

    def ver_contenido(self, obj):
        if obj.contenido_objeto:
            # Obtiene el título, comentario o representación en texto del objeto
            texto = getattr(
                obj.contenido_objeto, 
                'titulo', 
                getattr(obj.contenido_objeto, 'contenido', str(obj.contenido_objeto))
            )
            return format_html("<strong>[{}]</strong> {}", obj.content_type.model.upper(), texto[:50])
        return "Objeto eliminado"
    
    ver_contenido.short_description = 'Contenido Reportado'

    def save_model(self, request, save_obj, form, change):
        if save_obj.estado == 'aprobado':
            validar_reporte(save_obj)
        elif save_obj.estado == 'rechazado':
            invalidar_reporte(save_obj)
        else:
            super().save_model(request, save_obj, form, change)