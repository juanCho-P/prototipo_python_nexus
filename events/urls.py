from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.buscar_eventos,
        name='buscar_eventos'
    ),

    # Mis eventos
    path(
        'mis-eventos/',
        views.mis_eventos,
        name='mis_eventos'
    ),

    # Crear
    path(
        'crear/',
        views.crear_evento,
        name='crear_evento'
    ),

    # Detalle
    path(
        'detalle/<int:pk>/',
        views.detalle_evento,
        name='evento_detalle'
    ),

    # Editar
    path(
        'editar/<int:pk>/',
        views.editar_evento,
        name='editar_evento'
    ),

    # Unirse / retirarse
    path(
        'unirse/<int:pk>/',
        views.unirse_evento,
        name='unirse_evento'
    ),

    # Cancelar
    path(
        'cancelar/<int:pk>/',
        views.cancelar_evento,
        name='cancelar_evento'
    ),

    # Reportar
    path(
        'reportar/<int:pk>/',
        views.reportar_evento,
        name='reportar_evento'
    ),


 path(
     'cancelar-asistencia/<int:pk>/', 
      views.cancelar_asistencia,
       name='cancelar_asistencia'
    ),

 
]