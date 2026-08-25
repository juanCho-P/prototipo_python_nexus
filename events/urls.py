from django.urls import path
from . import views

urlpatterns = [

    # Buscar / listar eventos
    path(
        '',
        views.buscar_eventos,
        name='event_list'
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
]