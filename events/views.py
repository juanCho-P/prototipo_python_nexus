from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Evento
from .forms import EventoForm
from notification.models import Notificacion
from categorias.models import Categoria
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Reporte
from report.services import  usuario_ya_reporto

@login_required
def buscar_eventos(request):

    query = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')
    orden = request.GET.get('orden', 'proximos')

    
    eventos = Evento.objects.filter(estado='PUBLICADO').select_related('id_creador').prefetch_related('categoria', 'asistentes')

   
    for evento in eventos:
        actualizar_estado_evento(evento)

    
    eventos = eventos.filter(estado='PUBLICADO')

    if query:
        eventos = eventos.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query) | Q(ubicacion__icontains=query)
        )

    if categoria_id:
        eventos = eventos.filter(categoria__id=categoria_id)

    eventos = eventos.annotate(total_asistentes=Count('asistentes'))

   
    if orden == 'populares':
        eventos = eventos.order_by('-total_asistentes', 'f_inicio')
    elif orden == 'recientes':
        eventos = eventos.order_by('-created_at')
    else:  
        eventos = eventos.order_by('f_inicio')

    paginator = Paginator(eventos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categorias = Categoria.objects.all()

    return render(request, 'event/buscar_eventos.html', {
        'page_obj': page_obj,
        'categorias': categorias,
        'orden_actual': orden,
        'now': timezone.now()
    })


@login_required
def crear_evento(request):
    if not request.user.email_verificado:
        messages.error(request, 'Debes verificar tu correo electrónico para crear un evento.')
        return redirect('event_list')

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.id_creador = request.user
            
            
            evento.estado = 'PUBLICADO'
            
            evento.save()
            form.save_m2m() 

            messages.success(request, '¡Evento publicado con éxito!')
            return redirect('evento_detalle', pk=evento.pk) 
    else:
        form = EventoForm()

    return render(request, 'event/crear_evento.html', {
        'form': form, 
        'accion': 'Crear'
    })


@login_required
def mis_eventos(request):
    eventos = Evento.objects.filter(
        id_creador=request.user
    ).order_by('f_inicio')

    for evento in eventos: 
        actualizar_estado_evento(evento)
    
    return render(request, 'event/mis_eventos.html', {
        'eventos': eventos,
        'now': timezone.now()
    })

@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, id_creador=request.user)

    if evento.estado in ['FINALIZADO', 'CANCELADO']:
        messages.error(
            request,
            'Este evento ya no puede ser editado.'
        )
        return redirect('evento_detalle', pk=evento.pk)

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento actualizado correctamente.')
            return redirect('evento_detalle', pk=evento.pk) 
    else:
        form = EventoForm(instance=evento)
        
    return render(
        request, 
        'event/crear_evento.html', 
        {
            'form': form, 
            'evento': evento, 
            'accion': 'Editar'
        }
    )


@login_required
def unirse_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    actualizar_estado_evento(evento)

   
    if evento.id_creador == request.user:
        messages.warning(request, 'Eres el organizador de este evento.')
        return redirect('evento_detalle', pk=evento.pk)

    if not request.user.email_verificado:
        messages.error(
            request,
            'Debes verificar tu correo electrónico para unirte a un evento.'
        )
        return redirect('evento_detalle', pk=evento.pk)

    if evento.estado != 'PUBLICADO':
        messages.error(
            request,
            'No puedes unirte a un evento que no está publicado.'
        )
        return redirect('evento_detalle', pk=evento.pk)

    if evento.f_inicio <= timezone.now():
        messages.error(
            request,
            'No puedes unirte a un evento que ya ha comenzado.'
        )
        return redirect('evento_detalle', pk=evento.pk)

    if request.user in evento.asistentes.all():
        evento.asistentes.remove(request.user)
        messages.success(request, 'Te has retirado del evento.')
    else:
        evento.asistentes.add(request.user)
        messages.success(request, 'Te has unido al evento.')

    return redirect('evento_detalle', pk=evento.pk)

# Importa tu modelo de notificaciones

@login_required
def cancelar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

   
    if evento.id_creador != request.user:
        messages.error(request, 'No tienes permiso para cancelar este evento.')
        return redirect('detalle_evento', pk=pk)

    if request.method == 'POST':
        
        evento.estado = 'CANCELADO'
        evento.save(update_fields=['estado'])

  
        asistentes = evento.asistentes.all()
        notificaciones_crear = [
            Notificacion(
                usuario=asistente,
                evento=evento,
                tipo='EVENTO_CANCELADO',
                mensaje=f"El evento '{evento.titulo}' al que te uniste ha sido cancelado por el organizador."
            )
            for asistente in asistentes
        ]
        
      
        Notificacion.objects.bulk_create(notificaciones_crear)

        messages.success(request, 'El evento ha sido cancelado y se notificó a los participantes.')

    return redirect('detalle_evento', pk=pk)
@login_required
def reportar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    
   
    if evento.id_creador == request.user:
        messages.error(request, 'No puedes reportar tu propio evento.')
        return redirect('evento_detalle', pk=evento.pk)
        
   
    messages.info(request, 'Formulario de reporte en desarrollo.')
    return redirect('evento_detalle', pk=evento.pk) 


@login_required
def detalle_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    actualizar_estado_evento(evento)

    puede_ver = (
        evento.estado in ['PUBLICADO', 'FINALIZADO', 'CANCELADO']
        or evento.id_creador == request.user
    )

    if not puede_ver:
        messages.error(request, 'No tienes permiso para ver este evento.')
        return redirect('event_list')

    ya_asiste = evento.asistentes.filter(pk=request.user.pk).exists()

    ya_reporto = False
    if request.user.is_authenticated:
        ya_reporto = usuario_ya_reporto(request.user, evento)

    context = {
        'evento': evento,
        'now': timezone.now(),
        'ya_asiste': ya_asiste,
        'ya_reporto': ya_reporto,
        'total_asistentes': evento.asistentes.count(),
        'es_creador': (evento.id_creador == request.user),
        'motivos_reporte': Reporte.MOTIVOS_CHOICES
    }

    return render(request, 'event/evento_detalle.html', context)



# FUNCION AXILIAR PARA ACTUALIZAR LOS ESTADOS DE EVENTO
def actualizar_estado_evento(evento):
    ahora = timezone.now()

    if evento.estado == 'PUBLICADO' and evento.f_fin <= ahora:
        evento.estado = 'FINALIZADO'
        evento.save(update_fields=['estado'])