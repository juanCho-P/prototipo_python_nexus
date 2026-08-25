from django.db import models

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Reporte(models.Model):
    ESTADOS = [
        ('PENDIENTE','Pendiente'),
        ('VALIDO','Válido'),
        ('INVALIDO','Inválido'),
    ]

    MOTIVOS = [
        ('SPAM','Spam/Publicidad'),
        ('ACOSO','Acoso/Discriminación'),
        ('INAPROPIADO','Contenido inapropiado'),
        ('OTRO','Otro'),
    ]

    motivo = models.CharField(
        max_length=20,
          choices=MOTIVOS)
    
    comentario_adicional = models.TextField(
        blank=True, 
        null=True)

    estado = models.CharField(
        max_length=20, 
        choices=ESTADOS, 
        default='PENDIENTE')

    created_at = models.DateTimeField(
        auto_now_add=True)

    id_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete= models.CASCADE
    )

    object_id = models.BigIntegerField()

    contenido_reportado = GenericForeignKey(
        'content_type',
        'object_id'
    )

    def __str__(self):
        return f"Reporte de {self.id_usuario} sobre {self.contenido_reportado}"

  