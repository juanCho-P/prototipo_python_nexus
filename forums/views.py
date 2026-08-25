from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from categorias.models import Categoria
from .forms import ForoForm
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Foro, Comentario, ForoGuardado

# ============================================================
# EDITAR FORO
# ============================================================


@login_required
def editar_foro(request, foro_id):
    
    foro = get_object_or_404(Foro, id=foro_id)

  
    if foro.id_creador != request.user:
        messages.error(request, 'No tienes permisos para editar este foro.')
        return redirect('foro_detalle', foro_id=foro.id)

    if request.method == 'POST':
        form = ForoForm(request.POST, request.FILES, instance=foro)
        if form.is_valid():
            form.save()
            messages.success(request, 'El foro se ha actualizado correctamente.')
            return redirect('foro_detalle', foro_id=foro.id)
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
       
        form = ForoForm(instance=foro)

    return render(
        request,
        'forums/editar_foro.html',
        {
            'form': form,
            'foro': foro
        }
    )

# ============================================================
# VER TODOS LOS FOROS / BUSCAR
# ============================================================
def buscar_foro(request):
    query = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')
    orden = request.GET.get('orden', 'recientes')  # Valor por defecto: recientes

    foros = Foro.objects.filter(estado='PUBLICADO').select_related('id_creador').prefetch_related('categoria')

   
    if query:
        foros = foros.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query)
        )

    if categoria_id:
        foros = foros.filter(categoria__id=categoria_id)

   
    foros = foros.annotate(
        total_comentarios=Count('comentario', filter=Q(comentario__activo=True))
    )


    if orden == 'populares':
        foros = foros.order_by('-total_comentarios', '-created_at')
    else:
        foros = foros.order_by('-created_at')

   
    paginator = Paginator(foros, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categorias = Categoria.objects.all()

    return render(request, 'forums/buscar_foro.html', {
        'page_obj': page_obj,
        'categorias': categorias,
        'orden_actual': orden,
    })


@login_required
def detalle_foro(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)


    if foro.estado != 'PUBLICADO' and foro.id_creador != request.user:
        messages.error(request, 'Este foro no está disponible.')
        return redirect('buscar_foro')

    
    if request.method == 'POST':
        
        if foro.estado == 'ELIMINADO':
            messages.error(request, 'Este foro está desactivado y no acepta nuevas respuestas.')
            return redirect('foro_detalle', foro_id=foro.id)

        # Validar correo verificado
        if hasattr(request.user, 'email_verificado') and not request.user.email_verificado:
            messages.error(request, 'Debes verificar tu correo electrónico para comentar.')
            return redirect('foro_detalle', foro_id=foro.id)

        contenido = request.POST.get('contenido', '').strip()
        imagen_adjunta = request.FILES.get('imagen')    

        if not contenido and not imagen_adjunta:
            messages.error(request, 'El comentario no puede estar vacío.')
            return redirect('foro_detalle', foro_id=foro.id)

        comentario_padre_id = request.POST.get('comentario_padre')
        comentario_padre = None

        if comentario_padre_id:
            comentario_padre = get_object_or_404(
                Comentario,
                id=comentario_padre_id,
                id_foro=foro
            )

        Comentario.objects.create(
            respuesta=contenido,
            imagen=imagen_adjunta,
            id_foro=foro,
            id_usuario=request.user,
            comentario_padre=comentario_padre
        )

        messages.success(request, 'Comentario publicado correctamente.')
        return redirect('foro_detalle', foro_id=foro.id)

  
    publicaciones = (
        Comentario.objects
        .select_related('id_usuario', 'comentario_padre')
        .prefetch_related('respuestas__id_usuario')
        .filter(
            id_foro=foro,
            comentario_padre__isnull=True,
            activo=True
        )
        .order_by('-created_at') 
    )

  
    es_guardado = ForoGuardado.objects.filter(
        usuario=request.user, 
        foro=foro
    ).exists()

    return render(
        request,
        'forums/foro_detalle.html',
        {
            'foro': foro,
            'publicaciones': publicaciones,
            'es_guardado': es_guardado,
        }
    )
# ============================================================
# CREAR FORO
# ============================================================

@login_required
def crear_foro(request):
    if hasattr(request.user, 'email_verificado') and not request.user.email_verificado:
        messages.error(
            request,
            'Debes verificar tu correo electrónico para crear un foro.'
        )
        return redirect('buscar_foro')

    if request.method == 'POST':
        form = ForoForm(request.POST, request.FILES)
        if form.is_valid():
            foro = form.save(commit=False)
            foro.id_creador = request.user
            foro.save()
            form.save_m2m()  # Guarda las categorías de la relación ManyToMany

            messages.success(request, 'Foro creado correctamente.')
            return redirect('buscar_foro')
    else:
        form = ForoForm()

    return render(
        request,
        'forums/crear_foro.html',
        {'form': form}
    )


# ============================================================
# MIS FOROS
# ============================================================

@login_required
def mis_foros_view(request):

    query = request.GET.get(
        'search',
        ''
    ).strip()

    foros = Foro.objects.filter(
        id_creador=request.user
    ).order_by('-created_at')

    if query:

        foros = foros.filter(
            titulo__icontains=query
        )

    return render(
        request,
        'forums/forum_me.html',
        {
            'foros': foros,
            'query': query
        }
    )


# ============================================================
# ELIMINAR FORO
# ============================================================

@login_required
def eliminar_foro(request, foro_id):

    foro = get_object_or_404(
        Foro,
        id=foro_id,
        id_creador=request.user
    )

    foro.estado = 'ELIMINADO'

    foro.save(
        update_fields=['estado']
    )

    messages.success(
        request,
        'El foro ha sido eliminado.'
    )

    return redirect('buscar_foro')


# ============================================================
# ELIMINAR COMENTARIO
# ============================================================

def desactivar_comentario_y_descendientes(comentario):
    comentario.activo = False
    comentario.save(update_fields=['activo'])
    
    for respuesta in comentario.respuestas.filter(activo=True):
        desactivar_comentario_y_descendientes(respuesta)

@login_required
def eliminar_publicacion(request, pub_id):
    publicacion = get_object_or_404(Comentario, id=pub_id)
    foro_id = publicacion.id_foro.id

    if publicacion.id_usuario != request.user:
        messages.error(request, 'No puedes eliminar este comentario.')
        return redirect('foro_detalle', foro_id=foro_id)


    desactivar_comentario_y_descendientes(publicacion)

    messages.success(request, 'Comentario eliminado.')
    return redirect('foro_detalle', foro_id=foro_id)

# ============================================================
# REPORTAR CONTENIDO
# ============================================================

@login_required
def reportar_contenido(request):

    if request.method == 'POST':


        motivo = request.POST.get(
            'motivo'
        )

        comentario = request.POST.get(
            'comentario',
            ''
        )

        foro_id = request.POST.get(
            'foro_id'
        )

        pub_id = request.POST.get(
            'pub_id'
        )

      

        messages.success(
            request,
            'Reporte recibido correctamente.'
        )

    return redirect('buscar_foro')


@login_required
def guardar_foro_toggle(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)
    
   
    guardado, created = ForoGuardado.objects.get_or_create(
        usuario=request.user,
        foro=foro
    )
    
    if not created:
        guardado.delete()

    return redirect('foro_detalle', foro_id=foro.id)

@login_required
def mis_foros_guardados(request):
   
    foros_guardados = ForoGuardado.objects.filter(
        usuario=request.user
    ).select_related('foro', 'foro__id_creador').order_by('-created_at')

    return render(request, 'forums/mis_foros_guardados.html', {
        'foros_guardados': foros_guardados
    })
    guardados = ForoGuardado.objects.filter(usuario=request.user).select_related('foro').order_by('-created_at')
    return render(request, 'forums/foro_guardado.html', {'guardados': guardados})