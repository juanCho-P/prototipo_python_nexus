from django.urls import path
from . import views

urlpatterns = [
    path('marcar-todas/', views.marcar_todas_leidas, name='marcar_notificaciones_leidas'),
    path('marcar/<int:pk>/', views.marcar_como_leida, name='marcar_notificacion_leida'),
    path('eliminar/<int:pk>/', views.eliminar_notificacion, name='eliminar_notificacion'),
]