from django.http import HttpResponseForbidden

class RestringirAdminIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/gestion-secreta-nexus/'):
            ip_cliente = request.META.get('REMOTE_ADDR')
            ips_permitidas = ['127.0.0.1', 'TU_IP_PUBLICA_AQUI']
            if ip_cliente not in ips_permitidas:
                return HttpResponseForbidden('Acceso denegado desde esta red.')
        return self.get_response(request)