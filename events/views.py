from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Evento
from .forms import EventoForm

@login_required
def buscar_eventos(request):

    eventos = Evento.objects.filter(
        estado='PUBLICADO'
    ).order_by('f_inicio')

    for evento in eventos: actualizar_estado_evento(evento)
    
    
    query_busqueda = request.GET.get('q')


    if query_busqueda:
        eventos = eventos.filter(titulo__icontains=query_busqueda)
        
    return render(request, 'event/buscar_eventos.html', {
        'eventos': eventos,
        'now': timezone.now()
    })

@login_required
def  mis_eventos(request):
    eventos = Evento.objects.filter(
        id_creador=request.user
    ).order_by('f_inicio')

    for evento in eventos: actualizar_estado_evento(evento)
    
    return render(request, 'event/mis_eventos.html', {
        'eventos': eventos,
        'now': timezone.now()
    })


@login_required
def crear_evento(request):

    if not request.user.email_verificado:
        messages.error(
            request,
            'Debes verificar tu correo electrónico para crear un evento.'
        )
        return redirect('event_list')

    if request.method == 'POST':
        form = EventoForm(
            request.POST, 
            request.FILES
        )

        if form.is_valid():
            evento = form.save(commit=False)
            evento.id_creador = request.user
            evento.save()
            
            # Línea imprescindible para guardar la relación ManyToMany (categoría)
            form.save_m2m()

            return redirect(
                'evento_detalle',
                pk=evento.pk
            ) 
        
    else:
        form = EventoForm()

    return render(
        request, 
        'event/crear_evento.html',
        {
            'form': form, 
            'accion': 'Crear'
        }
    )

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
            return redirect('evento_detalle', pk=evento.pk) 
    else:
        form = EventoForm(instance=evento)
    return render(request, 'event/crear_evento.html', {'form': form, 'evento': evento, 'accion': 'Editar'})


@login_required
def unirse_evento(request, pk):

    evento = get_object_or_404(
        Evento,
        pk=pk
    )

    actualizar_estado_evento(evento)

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

    if evento.f_fin <= timezone.now():
        messages.error(
            request,
            'No puedes unirte a un evento que ya ha finalizado.'
        )
        return redirect('evento_detalle', pk=evento.pk)

    if request.user in evento.asistentes.all():

        evento.asistentes.remove(request.user)

        messages.success(
            request,
            'Te has retirado del evento.'
        )

    else:

        evento.asistentes.add(request.user)

        messages.success(
            request,
            'Te has unido al evento.'
        )

    return redirect(
        'evento_detalle',
        pk=evento.pk
    )

 

 


@login_required
def cancelar_evento(request, pk):

    evento = get_object_or_404(
        Evento,
        pk=pk,
        id_creador=request.user
    )

    evento.estado = 'CANCELADO'
    evento.save(update_fields=['estado'])

    messages.success(
        request,
        'El evento ha sido cancelado.'
    )

    return redirect('evento_detalle', pk=evento.pk)







@login_required

def reportar_evento(request, pk):
    return redirect('event_list') 


@login_required

def detalle_evento(request, pk):

    evento = get_object_or_404(
    Evento,
    pk=pk
    )
    actualizar_estado_evento(evento)

    puede_ver = (
        evento.estado == 'PUBLICADO'
        or(
            request.user.is_authenticated
            and evento.id_creador == request.user
        )
    )

    if not puede_ver:
        messages.error(
            request,
            'No tienes permiso para ver este evento.'
        )
        return redirect('event_list')

    ya_asiste = False

    if request.user.is_authenticated:
        ya_asiste = evento.asistentes.filter(
            pk = request.user.pk
        ).exists()

    return render(
        request,
        'event/evento_detalle.html',
        {
            'evento' : evento,
            'now' : timezone.now(),
            'ya_asiste': ya_asiste,
            'total_asistentes' : evento.asistentes.count(),
        }
    )



# FUNCION AXILIAR PARA ACTUALIZAR LOS ESTADOS DE EVENTO
def actualizar_estado_evento(evento):
    ahora = timezone.now()

    if evento.estado == 'PUBLICADO' and evento.f_fin <= ahora:
        evento.estado = 'FINALIZADO'
        evento.save(update_fields=['estado'])