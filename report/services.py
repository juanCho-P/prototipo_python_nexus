
def validar_reporte(reporte):

    reporte.estado = 'VALIDO'
    reporte.save(update_fields=['estado'])

    contenido = reporte.contenido_reportado

    if hasattr(contenido, 'id_usuario'):
        usuario = contenido.id_usuario

    elif hasattr(contenido, 'id_creador'):
        usuario = contenido.id_creador

    else:
        usuario = None

    if usuario:

        usuario.strikes += 1

        if usuario.strikes >= 3:
            usuario.estado = 'BLOQUEADO'
            usuario.is_active = False

        usuario.save(
            update_fields=[
                'strikes',
                'estado',
                'is_active'
            ]
        )


def invalidar_reporte(reporte):

    reporte.estado = 'INVALIDO'

    reporte.save(
        update_fields=['estado']
    )