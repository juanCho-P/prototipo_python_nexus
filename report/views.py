from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required


from report.models import Reporte
from forums.models import Foro,Comentario
from events.models import Evento
from .services import validar_reporte, invalidar_reporte


@login_required
def reportar_foro(request, foro_id):

    foro = get_object_or_404(
        Foro,
        id=foro_id
    )

    return crear_reporte(
        request,
        foro,
        'foro_detalle',
        foro_id=foro.id
    )


@login_required
def reportar_comentario(request, comentario_id):

    comentario = get_object_or_404(
        Comentario,
        id=comentario_id
    )

    return crear_reporte(
        request,
        comentario,
        'foro_detalle',
        foro_id=comentario.id_foro.id
    )

@login_required
def reportar_evento(request, evento_id):

    evento = get_object_or_404(
        Evento,
        id=evento_id
    )

    return crear_reporte(
        request,
        evento,
        'detalle_evento',
        evento_id=evento.id
    )

def crear_reporte(request, objeto, redirect_url, **redirect_kwargs):

    if request.method != 'POST':
        return redirect(redirect_url, **redirect_kwargs)

    motivo = request.POST.get('motivo')
    comentario_adicional = request.POST.get(
        'comentario_adicional',
        ''
    ).strip()

    motivos_validos = dict(Reporte.MOTIVOS)

    if motivo not in motivos_validos:
        messages.error(
            request,
            'El motivo seleccionado no es válido.'
        )
        return redirect(
            redirect_url,
            **redirect_kwargs
        )

    content_type = ContentType.objects.get_for_model(objeto)

    existe = Reporte.objects.filter(
        id_usuario=request.user,
        content_type=content_type,
        object_id=objeto.pk,
        estado='PENDIENTE'
    ).exists()

    if existe:
        messages.warning(
            request,
            'Ya has reportado este contenido.'
        )
        return redirect(
            redirect_url,
            **redirect_kwargs
        )

    Reporte.objects.create(
        id_usuario=request.user,
        content_type=content_type,
        object_id=objeto.pk,
        motivo=motivo,
        comentario_adicional=comentario_adicional
    )

    messages.success(
        request,
        'Reporte enviado correctamente.'
    )

    return redirect(
        redirect_url,
        **redirect_kwargs
    )

@staff_member_required
def validar_reporte_view(request, reporte_id):

    reporte = get_object_or_404(
        Reporte,
        id=reporte_id
    )

    validar_reporte(reporte)

    return redirect('lista_reportes')

@staff_member_required
def lista_reportes(request):

    reportes = Reporte.objects.select_related(
        'id_usuario',
        'content_type'
    ).order_by('-created_at')

    return render(
        request,
        'report/lista_reportes.html',
        {
            'reportes': reportes
        }
    )



@staff_member_required
def invalidar_reporte_view(request, reporte_id):

    reporte = get_object_or_404(
        Reporte,
        id=reporte_id
    )

    invalidar_reporte(reporte)

    return redirect('lista_reportes')
