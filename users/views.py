from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes

from events.models import Evento
from forums.models import Foro

from .models import Usuario
from .forms import RegistroForm, LoginForm, EditarPerfil, AvatarForm

# -------------------------------------------
# VISTAS PARA EL LOGIN, REGISTRO Y DASHBOARD
# -------------------------------------------

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            return JsonResponse({
                'success': False,
                'message': 'Por favor completa todos los campos.'
            }, status=400)

        # Autenticación segura de credenciales
        user = authenticate(request, username=username, password=password)

        if user is not None:
            #getattr verifica la existencia del atributo de forma segura sin lanzar AttributeError (500)
            es_verificado = getattr(user, 'email_verificado', True)

            if not es_verificado:
                return JsonResponse({
                    'success': False, 
                    'message': 'Tu correo no está verificado. Por favor, revísalo antes de iniciar sesión.'
                }, status=403)

            auth_login(request, user)
            return JsonResponse({
                'success': True, 
                'message': f'¡Bienvenido {user.username}!', 
                'redirect_url': reverse('dashboard')
            })
        else:
            return JsonResponse({
                'success': False, 
                'message': 'Usuario o contraseña incorrectos.'
            }, status=400)

    return render(request, 'users/auth.html')


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            enviar_correo_verificacion(request, user)

            return JsonResponse({
                'success': True, 
                'message': 'Cuenta creada exitosamente. Se ha enviado un enlace a tu correo.'
            })
        else:
            
            error_msg = next(iter(form.errors.values()))[0]
            return JsonResponse({'success': False, 'message': error_msg}, status=400)

    return render(request, 'users/auth.html', {'form': RegistroForm()})


@login_required
def dashboard(request):
    eventos = Evento.objects.filter(id_creador=request.user)
    foros = Foro.objects.filter(id_creador=request.user)

    total_asistentes = sum(
        evento.asistentes.count()
        for evento in eventos
    )

    context = {
        'eventos': eventos,
        'foros': foros,
        'total_eventos': eventos.count(),
        'total_foros': foros.count(),
        'total_asistentes': total_asistentes
    }

    return render(request, 'dashboard/dashboardUser.html', context)


# ---------------------------------
# VISTAS PARA EL PERFIL DEL USUARIO
# ---------------------------------

@login_required
def perfil_view(request):
    usuario = request.user
    return render(request, 'users/perfil.html', {'usuario': usuario})


@login_required
def editar_perfil(request):
    usuario = request.user

    if request.method == 'POST':
        email_anterior = usuario.email

        form = EditarPerfil(
            request.POST,
            instance=usuario
        )

        if form.is_valid():
            usuario = form.save()

            if usuario.email != email_anterior:
                usuario.email_verificado = False
                usuario.save(update_fields=['email_verificado'])

                # Reenvío de correo al cambiar la dirección email
                enviar_correo_verificacion(request, usuario)

                messages.warning(
                    request,
                    "Has cambiado tu correo. Te hemos enviado un nuevo mensaje para verificar tu nueva dirección."
                )
            else:
                messages.success(request, "Perfil actualizado correctamente.")

            return redirect('perfil')

    else:
        form = EditarPerfil(instance=usuario)

    return render(request, 'users/editar_perfil.html', {'form': form})


@login_required
def cambiar_avatar(request):
    usuario = request.user

    if request.method == 'POST':
        form = AvatarForm(
            request.POST,
            request.FILES,
            instance=usuario
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Avatar actualizado correctamente.")
            return redirect('perfil')

    else:
        form = AvatarForm(instance=usuario)

    return render(request, 'users/cambiar_avatar.html', {'form': form})


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


# ---------------------------------
# SERVICIOS Y VERIFICACIÓN DE EMAIL
# ---------------------------------

def enviar_correo_verificacion(request, usuario):
    if usuario.email_verificado:
        return

    uid = urlsafe_base64_encode(force_bytes(usuario.pk))
    token = default_token_generator.make_token(usuario)

    enlace = request.build_absolute_uri(
        reverse(
            'verificar_email',
            kwargs={
                'uidb64': uid,
                'token': token
            }
        )
    )

    mensaje = (
        f"Hola {usuario.username},\n\n"
        "Por favor, haz clic en el siguiente enlace "
        "para verificar tu correo electrónico:\n\n"
        f"{enlace}\n\n"
        "Si no solicitaste esta verificación, puedes ignorar este mensaje."
    )

    send_mail(
        'Verificación de correo electrónico',
        mensaje,
        None,
        [usuario.email],
    )


def verificar_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        usuario = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        usuario = None

    if usuario is not None and default_token_generator.check_token(usuario, token):
        usuario.email_verificado = True
        usuario.save(update_fields=['email_verificado'])

        messages.success(
            request,
            "¡Correo electrónico verificado correctamente!"
        )
        return redirect('auth')

    messages.error(
        request,
        "El enlace de verificación es inválido o ha expirado."
    )
    return redirect('auth')


def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('auth')


def auth_view(request):
    return render(request, 'users/auth.html')