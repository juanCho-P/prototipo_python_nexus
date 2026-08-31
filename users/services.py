import os

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


def enviar_correo_verificacion(email_destino, token_verificacion):

    # Configurar la autenticación con tu Clave API de Brevo
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    enlace_verificacion = (
        f"https://nexus-hpqz.onrender.com/users/verify/{token_verificacion}/"
    )

    # Estructura del correo para la API de Brevo
    sender = {
        "name": "Nexus App",
        "email": "equiponexus687@gmail.com"
    }

    to = [{"email": email_destino}]

    html_content = f"""
        <div style="font-family: sans-serif; color: #333;">
            <h2>¡Bienvenido a Nexus!</h2>

            <p>
                Haz clic en el siguiente botón para verificar tu cuenta de correo:
            </p>

            <a href="{enlace_verificacion}"
               style="background: #4f46e5; color: white; padding: 10px 20px;
                      text-decoration: none; border-radius: 5px;
                      display: inline-block;">
                Verificar correo
            </a>
        </div>
    """

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        sender=sender,
        to=to,
        subject="Verificación de cuenta - Nexus",
        html_content=html_content
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return api_response

    except ApiException as e:
        print(f"Error enviando correo con la API de Brevo: {e}")
        return None