from django.db import transaction
from .models import Reporte

from django.contrib.contenttypes.models import ContentType

def validar_reporte(reporte):
    if reporte.estado != 'PENDIENTE':
        return False

    with transaction.atomic():
        objeto = reporte.contenido_objeto  
        autor_infractor = None

        
        if hasattr(objeto, 'id_creador') and objeto.id_creador:
            autor_infractor = objeto.id_creador
        elif hasattr(objeto, 'id_usuario') and objeto.id_usuario:
            autor_infractor = objeto.id_usuario

        if autor_infractor:
            
            autor_infractor.strikes = getattr(autor_infractor, 'strikes', 0) + 1
            
           
            if autor_infractor.strikes >= 3:
                autor_infractor.is_active = False

            autor_infractor.save()

           
            if hasattr(reporte, 'reportado'):
                reporte.reportado = autor_infractor

        reporte.estado = 'APROBADO'
        reporte.save()

    return True

def invalidar_reporte(reporte):
    if reporte.estado == 'PENDIENTE':
        reporte.estado = 'RECHAZADO'
        reporte.save()
        return True
    return False





def usuario_ya_reporto(usuario, objeto):
    content_type = ContentType.objects.get_for_model(objeto)
    return Reporte.objects.filter(
        reportador=usuario,
        content_type=content_type,
        object_id=objeto.pk,
        estado='PENDIENTE'
    ).exists()