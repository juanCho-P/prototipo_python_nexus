from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notificacion

@login_required
def marcar_como_leida(request, pk):
    notificacion = get_object_or_404(Notificacion, pk=pk, usuario=request.user)
    notificacion.leido = True
    notificacion.save(update_fields=['leido'])
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

@login_required
def marcar_todas_leidas(request):
    if request.method == 'POST':
        Notificacion.objects.filter(usuario=request.user, leido=False).update(leido=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def eliminar_notificacion(request, pk):
    notificacion = get_object_or_404(Notificacion, pk=pk, usuario=request.user)
    notificacion.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        unread_count = Notificacion.objects.filter(usuario=request.user, leido=False).count()
        return JsonResponse({'status': 'success', 'unread_count': unread_count})
        
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))