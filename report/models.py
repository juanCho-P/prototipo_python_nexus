from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Reporte(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    )

    MOTIVOS_CHOICES = [
        ('SPAM', 'Contenido No Deseado / Spam'),
        ('INAPROPIADO', 'Contenido Inapropiado'),
        ('INCOMPLETO', 'Información Falsa o Engañosa'),
        ('OTRO', 'Otro motivo'),
    ]

    reportador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reportes_enviados',
        null=True,
        blank=True
    )
    reportado = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reportes_recibidos',
        null=True,
        blank=True
    )

    motivo = models.CharField(max_length=50, choices=MOTIVOS_CHOICES)
    comentario = models.TextField(blank=True, null=True)
   
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    contenido_objeto = GenericForeignKey('content_type', 'object_id')

    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Manejo seguro para evitar 'NoneType' object has no attribute 'username'
        usuario_reportado = self.reportado.username if self.reportado else "Usuario eliminado"
        tipo_contenido = self.content_type.model if self.content_type else "Objeto"
        
        return f"Reporte a {usuario_reportado} [{tipo_contenido}]"