from django.contrib import admin
from django.contrib import messages
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
    list_display = ('id', 'reportador', 'reportado', 'content_type', 'motivo', 'estado', 'created_at')
    list_filter = ('estado', 'content_type', 'created_at')
    search_fields = ('reportador__username', 'reportado__username', 'motivo')
    actions = [aprobar_reportes_action, rechazar_reportes_action]