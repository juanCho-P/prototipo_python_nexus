from datetime import datetime

from django.conf import settings
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect

class InactivityTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Tiempo de inactividad permitido (ej. 30 minutos)
        self.timeout = getattr(settings, 'INACTIVITY_TIMEOUT', 1800)

    def __call__(self, request):
        if request.user.is_authenticated:
            now = datetime.now().timestamp()
            last_activity = request.session.get('last_activity', now)
            
            # Comprobar si ha superado el tiempo límite
            if now - last_activity > self.timeout:
                logout(request)
                messages.warning(request, "Tu sesión ha expirado por inactividad.")
                return redirect(reverse('login'))
            
            # Actualizar la marca de tiempo de la última actividad
            request.session['last_activity'] = now

        response = self.get_response(request)
        return response