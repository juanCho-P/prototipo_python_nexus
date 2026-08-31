from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect

from events.models import Evento
from forums.models import Foro
from notification.models import Notificacion

from .models import Usuario
from .forms import RegistroForm, EditarPerfil
from .services import enviar_correo_verificacion


def generar_enlace_verificacion(request, user):
    """Función auxiliar para generar la URL absoluta con el uid y el token de verificación."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return request.build_absolute_uri(
        reverse('verificar_email', kwargs={'uidb64': uid, 'token': token})
    )


@login_required
def marcar_notificaciones_leidas(request):
    if request.method == 'POST':
        Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            return JsonResponse({'success': False, 'message': 'Por favor completa todos los campos.'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.strikes >= 3 or not user.is_active:
                return JsonResponse({
                    'success': False,
                    'is_blocked': True,
                    'message': 'Tu cuenta ha sido bloqueada por acumulación de strikes.'
                }, status=403)

            if not user.email_verificado:
                return JsonResponse({
                    'success': False, 
                    'message': 'Tu correo no está verificado.'
                }, status=403)

            auth_login(request, user)
            return JsonResponse({'success': True, 'message': f'¡Bienvenido {user.username}!', 'redirect_url': reverse('dashboard')})
        
        return JsonResponse({'success': False, 'message': 'Usuario o contraseña incorrectos.'}, status=400)

    return render(request, 'users/auth.html')


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            enlace = generar_enlace_verificacion(request, user)
            enviar_correo_verificacion(user.email, enlace)
            
            return JsonResponse({'success': True, 'message': 'Cuenta creada exitosamente. Verifica tu correo.'})
        
        error_msg = next(iter(form.errors.values()))[0]
        return JsonResponse({'success': False, 'message': error_msg}, status=400)

    return render(request, 'users/auth.html', {'form': RegistroForm()})


@login_required
def dashboard_view(request):
    usuario = request.user
    if usuario.strikes >= 3:
        messages.error(request, "Tu cuenta ha sido bloqueada temporalmente.")
        return redirect('logout')

    eventos = Evento.objects.filter(id_creador=usuario).prefetch_related('asistentes').order_by('-f_inicio')
    foros = Foro.objects.filter(id_creador=usuario).order_by('-created_at')
    eventos_usuario = Evento.objects.filter(asistentes=usuario).order_by('f_inicio')
    evento_proximo = eventos_usuario.filter(f_inicio__gte=timezone.now()).first()
    
    context = {
        'eventos': eventos,
        'eventos_usuario': eventos_usuario,
        'evento_proximo': evento_proximo,
        'foros': foros,
        'total_eventos': eventos.count(),
        'total_foros': foros.count(),
        'total_asistentes': sum(e.asistentes.count() for e in eventos),
        'evento_top': eventos.annotate(num_asistentes=Count('asistentes')).order_by('-num_asistentes').first(),
        'strikes_count': usuario.strikes,
    }
    return render(request, 'dashboard/dashboardUser.html', context)


@login_required
def perfil_view(request):
    return render(request, 'users/perfil.html', {'usuario': request.user})


@login_required
def editar_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        email_anterior = usuario.email
        form = EditarPerfil(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            if usuario.email != email_anterior:
                usuario.email_verificado = False
                usuario.save(update_fields=['email_verificado'])
                
                enlace = generar_enlace_verificacion(request, usuario)
                enviar_correo_verificacion(usuario.email, enlace)
                
                messages.warning(request, "Has cambiado tu correo. Verifica tu nueva dirección.")
            else:
                messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil')
    else:
        form = EditarPerfil(instance=usuario)
    return render(request, 'users/editar_perfil.html', {'form': form})


@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            usuario = form.save()
            update_session_auth_hash(request, usuario)
            messages.success(request, "Contraseña actualizada correctamente.")
            return redirect('perfil')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/cambiar_contrasena.html', {'form': form})


def verificar_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        usuario = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        usuario = None

    if usuario is not None and default_token_generator.check_token(usuario, token):
        usuario.email_verificado = True
        usuario.save(update_fields=['email_verificado'])
        messages.success(request, "¡Correo electrónico verificado correctamente!")
        return redirect('auth')

    messages.error(request, "El enlace de verificación es inválido o ha expirado.")
    return redirect('auth')


def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('auth')


def auth_view(request):
    return render(request, 'users/auth.html')


def provocate_500(request):
    return HttpResponse(1 / 0)