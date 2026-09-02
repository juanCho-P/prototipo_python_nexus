import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.core.mail.backends.base import BaseEmailBackend

def enviar_correo_verificacion(email_destino, enlace_verificacion):
   
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

   
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
    





class BrevoEmailBackend(BaseEmailBackend):
  

    def send_messages(self, email_messages):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        sender = {"name": "Nexus App", "email": "equiponexus687@gmail.com"}
        sent_count = 0

        for message in email_messages:
            
            html_content = f"<pre style='font-family: sans-serif;'>{message.body}</pre>"

            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                sender=sender,
                to=[{"email": r} for r in message.to],
                subject=message.subject,
                html_content=html_content,
            )
            try:
                api_instance.send_transac_email(send_smtp_email)
                sent_count += 1
            except ApiException as e:
                print(f"Error enviando correo con la API de Brevo: {e}")
                if not self.fail_silently:
                    raise

        return sent_count