from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from .models import Reporte
from .services import usuario_ya_reporto
from forums.models import Foro, Comentario
from events.models import Evento


@login_required
def reportar_foro(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)
    return crear_reporte(request, foro, 'foro_detalle', foro_id=foro.id)


@login_required
def reportar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    return crear_reporte(request, comentario, 'foro_detalle', foro_id=comentario.id_foro.id)


@login_required
def reportar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return crear_reporte(request, evento, 'evento_detalle', pk=evento.id)




def crear_reporte(request, objeto, redirect_url, **redirect_kwargs):
    if request.method != 'POST':
        return redirect(redirect_url, **redirect_kwargs)

    # 1. Identificar al autor del contenido
    autor = getattr(objeto, 'id_creador', None) or getattr(objeto, 'id_usuario', None)

    # 2. Validar que no auto-reporte su contenido
    if autor == request.user:
        messages.error(request, 'No puedes reportar tu propio contenido.')
        return redirect(redirect_url, **redirect_kwargs)

    # 3. Validar motivo seleccionado
    motivo_clave = request.POST.get('motivo')
    comentario_texto = request.POST.get('comentario_adicional', '').strip()
    motivos_validos = dict(Reporte.MOTIVOS_CHOICES)

    if motivo_clave not in motivos_validos:
        messages.error(request, 'El motivo seleccionado no es válido.')
        return redirect(redirect_url, **redirect_kwargs)

    # 4. Validar si ya existe un reporte PENDIENTE previo
    if usuario_ya_reporto(request.user, objeto):
        messages.warning(request, 'Ya has reportado este contenido y está pendiente de revisión.')
        return redirect(redirect_url, **redirect_kwargs)

    # 5. Formatear la información y guardar en el campo 'motivo'
    motivo_etiqueta = motivos_validos[motivo_clave]
    motivo_completo = f"[{motivo_etiqueta}] {comentario_texto}".strip()

    content_type = ContentType.objects.get_for_model(objeto)

    Reporte.objects.create(
        reportador=request.user,
        reportado=autor,
        content_type=content_type,
        object_id=objeto.pk,
        motivo=motivo_completo,
    )

    messages.success(request, 'Reporte enviado correctamente a los moderadores.')
    return redirect(redirect_url, **redirect_kwargs)