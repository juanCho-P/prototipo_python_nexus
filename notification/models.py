from django.db import models
from django.conf import settings
from events.models import Evento

class Notificacion(models.Model):
    TIPOS = [
        ('EVENTO_CANCELADO', 'Evento cancelado'),
        ('EVENTO_FINALIZADO', 'Evento finalizado'),
        ('NUEVO_EVENTO', 'Nuevo evento'),
        ('NUEVO_COMENTARIO', 'Nuevo comentario'),
        ('REPORTE', 'Reporte'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )

    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='Notificaciones'
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPOS
    )

    titulo = models.CharField(
        max_length=100,
        default="Notificación"
    )

    mensaje = models.CharField(
        max_length=255
    )

    leido = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.mensaje}"

    @property
    def es_warning(self):
        return self.tipo in ['EVENTO_CANCELADO', 'REPORTE']