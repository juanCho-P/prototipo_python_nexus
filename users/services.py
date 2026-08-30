import os
import resend
from django.conf import settings

def enviar_correo_verificacion(email_destino, token_verificacion):
    resend.api_key = os.environ.get('RESEND_API_KEY')
    
    params = {
        "from": "Nexus <onboarding@resend.dev>",
        "to": [email_destino],
        "subject": "Verificación de cuenta - Nexus",
        "html": f"""
            <div style="font-family: sans-serif; color: #333;">
                <h2>¡Bienvenido a Nexus!</h2>
                <p>Haz clic en el siguiente botón para verificar tu cuenta de correo:</p>
                <a href="https://nexus-hpqz.onrender.com/users/verify/{token_verificacion}/" 
                   style="background: #4f46e5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Verificar correo
                </a>
            </div>
        """,
    }
    
    try:
        response = resend.Emails.send(params)
        return response
    except Exception as e:
        print(f"Error enviando correo con Resend: {e}")
        return None