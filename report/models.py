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
        blank= True
    )


    motivo = models.CharField(max_length=50, choices=MOTIVOS_CHOICES)
    comentario = models.TextField(blank=True, null=True)
   
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    contenido_objeto = GenericForeignKey('content_type', 'object_id')

    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte a {self.reportado.username} [{self.content_type.model}]"