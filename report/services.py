from django.db import transaction
from .models import Reporte

from django.contrib.contenttypes.models import ContentType

def validar_reporte(reporte):
    if reporte.estado != 'PENDIENTE':
        return False

    with transaction.atomic():
        objeto = reporte.contenido_objeto  
        autor_infractor = None

        
# report/services.py
from django.db import transaction

def validar_reporte(reporte):
   
    if reporte.estado == 'aprobado':
        return False

    with transaction.atomic():
       
        reporte.estado = 'aprobado'
        reporte.save()

        
        usuario = reporte.reportado
        if usuario:
            usuario.strikes = getattr(usuario, 'strikes', 0) + 1
            
            if usuario.strikes >= 3:
                usuario.is_active = False
                
            usuario.save()
            return True

    return False


def invalidar_reporte(reporte):
    if reporte.estado == 'rechazado':
        return False
        
    reporte.estado = 'rechazado'
    reporte.save()
    return True




def usuario_ya_reporto(usuario, objeto):
    content_type = ContentType.objects.get_for_model(objeto)
    return Reporte.objects.filter(
        reportador=usuario,
        content_type=content_type,
        object_id=objeto.pk,
        estado='PENDIENTE'
    ).exists()