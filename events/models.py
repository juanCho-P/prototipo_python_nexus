from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from categorias.models import Categoria
from report.models import Reporte


class Evento(models.Model):
    ESTADOS = [
        ('BORRADOR', 'borrador'),
        ('PUBLICADO', 'Publicado'),
        ('CANCELADO', 'cancelado'),
        ('FINALIZADO', 'finalizado')
    ]
    
    imagen = models.ImageField(
        upload_to='eventos-img',
        null=True,
        blank=True
    )
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    ubicacion = models.CharField(
        max_length=255,
        null=True, 
        blank=True
    )
    
    f_inicio = models.DateTimeField()
    f_fin = models.DateTimeField()
    categoria = models.ManyToManyField(Categoria)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='BORRADOR'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    # Relacion con el usuario (Creador del evento)
    id_creador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='eventos_creados'
    )
  
    asistentes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='eventos_asistidos', 
        blank=True
    )

    # Relación genérica para reportes
    reportes = GenericRelation(Reporte)
    
    def __str__(self):
        return self.titulo