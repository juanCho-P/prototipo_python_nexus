from django.db import models 
from django.conf import settings 
from django.contrib.contenttypes.fields import GenericRelation
from categorias.models import Categoria
from report.models import Reporte


class Foro(models.Model): 
    ESTADOS = [
        ('PUBLICADO', 'Publicado'),
        ('OCULTO', 'Oculto por moderación'),
        ('ELIMINADO', 'Eliminado por el creador'),
        ('ELIMINADO_ADMIN', 'Eliminado por un administrador'),
    ]

    titulo = models.CharField(max_length=255) 
    descripcion = models.TextField() 
    categoria = models.ManyToManyField(Categoria)
    imagen = models.ImageField(upload_to="img-foros/", null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
    
    id_creador = models.ForeignKey( 
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True 
    )

    estado = models.CharField(max_length=20, choices=ESTADOS, default='PUBLICADO')
    reportes = GenericRelation(Reporte)

    def __str__(self):
        return self.titulo


class Comentario(models.Model): 
    respuesta = models.TextField() 
    imagen = models.ImageField(upload_to="comentarios-img/%Y/%m", null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    id_foro = models.ForeignKey(Foro, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True 
    )

    comentario_padre = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='respuestas'
    )

    activo = models.BooleanField(default=True) 
    reportes = GenericRelation(Reporte)

    def __str__(self):
        return f"{self.respuesta} por {self.id_usuario}"


class ForoGuardado(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='foros_guardados')
    foro = models.ForeignKey(Foro, on_delete=models.CASCADE, related_name='guardado_por')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'foro')

    def __str__(self):
        return f"{self.usuario} guardó {self.foro.titulo}"