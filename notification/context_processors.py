from notification.models import Notificacion

def notificaciones_usuario(request):
    if request.user.is_authenticated:
        # Obtiene las notificaciones del usuario actual
        notificaciones = Notificacion.objects.filter(
            usuario=request.user
        ).order_by('-created_at')[:10]
        
        # Conteo exacto que busca la campana en el HTML
        unread_notifications_count = Notificacion.objects.filter(
            usuario=request.user, 
            leido=False
        ).count()
        
        return {
            'notificaciones': notificaciones,                  # Coincide con {% if notificaciones %}
            'unread_notifications_count': unread_notifications_count,  # Coincide con {% if unread_notifications_count %}
        }
        
    return {
        'notificaciones': [],
        'unread_notifications_count': 0,
    }