from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def enviar_correo_verificacion(request, usuario):
    if usuario.email_verificado:
        return

    uid = urlsafe_base64_encode(force_bytes(usuario.pk))
    token = default_token_generator.make_token(usuario)

    enlace = request.build_absolute_uri(
        reverse('verificar_email', kwargs={'uidb64': uid, 'token': token})
    )

    mensaje = (
        f"Hola {usuario.username},\n\n"
        "Por favor, haz clic en el siguiente enlace para verificar tu correo electrónico:\n\n"
        f"{enlace}\n\n"
        "Si no solicitaste esta verificación, puedes ignorar este mensaje."
    )

    send_mail(
        'Verificación de correo electrónico',
        mensaje,
        None,
        [usuario.email],
    )