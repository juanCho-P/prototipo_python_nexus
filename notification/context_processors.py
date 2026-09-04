from notification.models import Notificacion

def notificaciones_usuario(request):
    if request.user.is_authenticated:
        
        notificaciones = Notificacion.objects.filter(
            usuario=request.user
        ).order_by('-created_at')[:10]
     
        unread_notifications_count = Notificacion.objects.filter(
            usuario=request.user, 
            leido=False
        ).count()
        
        return {
            'notificaciones': notificaciones,                  
            'unread_notifications_count': unread_notifications_count,  
        }
        
    return {
        'notificaciones': [],
        'unread_notifications_count': 0,
    }