from django.core.mail import send_mail
from django.conf import settings

def enviar_correo_verificacion(email_destino, token_verificacion):
    asunto = "Verificación de cuenta - Nexus"
    
    # URL de verificación apuntando a tu despliegue en Render
    enlace_verificacion = f"https://nexus-hpqz.onrender.com/users/verify/{token_verificacion}/"
    
    mensaje_html = f"""
        <div style="font-family: sans-serif; color: #333;">
            <h2>¡Bienvenido a Nexus!</h2>
            <p>Haz clic en el siguiente botón para verificar tu cuenta de correo:</p>
            <a href="{enlace_verificacion}" 
               style="background: #4f46e5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Verificar correo
            </a>
        </div>
    """
    
    try:
        # send_mail requiere texto plano como alternativa y el parámetro html_message para contenido enriquecido
        response = send_mail(
            subject=asunto,
            message="Haz clic en el enlace para verificar tu cuenta: " + enlace_verificacion,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_destino],
            html_message=mensaje_html,
            fail_silently=False,
        )
        return response
    except Exception as e:
        print(f"Error enviando correo con Brevo SMTP: {e}")
        return None